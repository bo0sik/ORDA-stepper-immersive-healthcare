import serial, threading, time
from pythonosc.udp_client import SimpleUDPClient
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# =========================
# OSC / 아두이노 설정
# =========================
UE_IP    = "127.0.0.1"  # 언리얼 IP
UE_PORT  = 10000        # 언리얼 OSC 포트

SER_PORT = "COM6"       # 아두이노 포트
BAUD     = 9600         # 아두이노 보드레이트

# OSC 클라이언트 & 시리얼 열기
osc = SimpleUDPClient(UE_IP, UE_PORT)
print(f"[OK] Gaze+Foot OSC → UE {UE_IP}:{UE_PORT}")

ser = serial.Serial(SER_PORT, BAUD, timeout=1)
print(f"[OK] Serial {SER_PORT}@{BAUD} 연결 완료")

# 아두이노 센서 상태 표시용
sensor_data = {"left": "idle", "right": "idle", "last": "none"}

def send_sensor(addr):
    """발 센서 이벤트를 OSC로 전송"""
    osc.send_message(addr, 1)

def serial_thread():
    """
    아두이노에서 'R' 또는 'L' 수신 → OSC 전송 + 상태 업데이트
    예: R = 오른발, L = 왼발
    """
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
        except Exception as e:
            print("[Serial Error]", e)
            continue

        if not line:
            continue

        low = line.lower()
        if low == "r":
            send_sensor("/sensor/right_up")
            sensor_data["right"] = "step"
        elif low == "l":
            send_sensor("/sensor/left_up")
            sensor_data["left"] = "step"

        sensor_data["last"] = line
        print(f"[SENSOR] {line}")

# 시리얼 스레드 시작
threading.Thread(target=serial_thread, daemon=True).start()

# =========================
# 시선 추적 설정
# ========================= 
NUM_COLS = 3                 # 존 개수(라벨용)
DRAW_DEBUG = True            # 디버그 그리기
SMOOTH_ALPHA = 0.2           # 픽셀 좌표 스무딩(화면 디버그 점용)
MIRROR = True                # 거울 모드
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ---- 시선 비율(0~1)용 필터 파라미터 ----
DEADZONE_NEAR   = 0.04
DEADZONE_FAR    = 0.015
ALPHA_NEAR      = 0.14
ALPHA_FAR       = 0.28
MEDIAN_WINDOW   = 7
SEND_THRESHOLD  = 0.012

CENTER_SNAP_RANGE = 0.04
CENTER_VALUE       = 0.5

# ★ 존 폭 비대칭 설정 (왼쪽/가운데/오른쪽 경계 비율) -----------------
LEFT_END_RATIO    = 0.20   # 왼쪽 존 끝 (0.0 ~ 0.20)
RIGHT_START_RATIO = 0.80   # 오른쪽 존 시작 (0.80 ~ 1.0)
# 가운데 존은 자동으로 0.20 ~ 0.80 구간
# -------------------------------------------------------------

# =========================
# Mediapipe 초기화
# =========================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# =========================
# 유틸: 지수이동평균(EMA) 스무딩
# =========================
def ema_update(prev, new, alpha=0.2):
    if prev is None:
        return new
    return (1 - alpha) * prev + alpha * new

# =========================
# 유틸: 시선 포인트 계산
# =========================
def get_iris_center(landmarks, idxs):
    xs = [landmarks[i].x for i in idxs]
    ys = [landmarks[i].y for i in idxs]
    return np.mean(xs), np.mean(ys)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# Mediapipe 인덱스
RIGHT_EYE_OUTER = 33   # 귀쪽
RIGHT_EYE_INNER = 133  # 코쪽
RIGHT_IRIS = [474, 475, 476, 477]  # 오른쪽 홍채

LEFT_EYE_INNER = 263   # 코쪽
LEFT_EYE_OUTER = 362   # 귀쪽
LEFT_IRIS = [469, 470, 471, 472]   # 왼쪽 홍채

# =========================
# 메인
# =========================
cap = cv2.VideoCapture(0)

smoothed_px = None
smoothed_py = None
prev_zone = None  # 칸이 바뀔 때만 이벤트 발생시키고 싶다면 사용

# 정규화 시선 비율용 스무딩 / 상태 변수
smoothed_ratio_x = None
smoothed_ratio_y = None
history_ratio_x = deque(maxlen=MEDIAN_WINDOW)

last_sent_ratio_x = None     # 마지막으로 OSC로 보낸 값

def on_zone_change(zone_idx):
    """칸이 바뀔 때 호출되는 훅(hook)."""
    label = chr(ord('A') + zone_idx)  # A, B, C
    print(f"[ZONE] -> {label}")
    osc.send_message("/gaze/zone", int(zone_idx))
    osc.send_message("/gaze/zone_label", label)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if MIRROR:
        frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    gaze_px, gaze_py = None, None

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        # 각 눈의 코쪽/귀쪽 모서리
        re_outer = face_landmarks[RIGHT_EYE_OUTER]  # 귀쪽
        re_inner = face_landmarks[RIGHT_EYE_INNER]  # 코쪽
        le_inner = face_landmarks[LEFT_EYE_INNER]   # 코쪽
        le_outer = face_landmarks[LEFT_EYE_OUTER]   # 귀쪽

        # 홍채 중심
        rix, riy = get_iris_center(face_landmarks, RIGHT_IRIS)
        lix, liy = get_iris_center(face_landmarks, LEFT_IRIS)

        # 1) raw 비율 (0=코쪽, 1=귀쪽)
        re_span = (re_outer.x - re_inner.x)
        if abs(re_span) < 1e-6:
            re_span = 1e-6
        r_ratio_x = (rix - re_inner.x) / re_span

        le_span = (le_outer.x - le_inner.x)
        if abs(le_span) < 1e-6:
            le_span = 1e-6
        l_ratio_x = (lix - le_inner.x) / le_span

        raw_ratio_x = clamp(0.5 * (r_ratio_x + l_ratio_x), 0.0, 1.0)
        raw_ratio_y = clamp(0.5 * (riy + liy), 0.0, 1.0)

        # === 2) 중앙값 필터 + 거리 기반(정면↔양옆) 데드존/EMA ===
        history_ratio_x.append(raw_ratio_x)
        median_ratio_x = float(np.median(history_ratio_x))

        # 정면에서 얼마나 떨어져있는지
        dist_from_center = abs(median_ratio_x - 0.5)

        # 정면 근처냐, 양옆이냐에 따라 파라미터 다르게
        if dist_from_center > 0.18:   # 꽤 왼쪽/오른쪽으로 간 상태
            deadzone = DEADZONE_FAR
            alpha    = ALPHA_FAR
        else:                         # 정면 근처
            deadzone = DEADZONE_NEAR
            alpha    = ALPHA_NEAR

        if smoothed_ratio_x is None:
            smoothed_ratio_x = median_ratio_x
            smoothed_ratio_y = raw_ratio_y
        else:
            # X축 데드존 적용
            dx = median_ratio_x - smoothed_ratio_x
            if abs(dx) < deadzone:
                median_ratio_x = smoothed_ratio_x

            # Y축도 간단히 데드존 처리
            dy = raw_ratio_y - smoothed_ratio_y
            if abs(dy) < deadzone:
                raw_ratio_y = smoothed_ratio_y

            # EMA 스무딩 (거리 기반 알파 사용)
            smoothed_ratio_x = ema_update(smoothed_ratio_x, median_ratio_x, alpha=alpha)
            smoothed_ratio_y = ema_update(smoothed_ratio_y, raw_ratio_y,    alpha=alpha)

        # === 3) 정면 근처에서는 센터로 스냅 (여기서 마지막으로 고정) ===
        if abs(smoothed_ratio_x - CENTER_VALUE) < CENTER_SNAP_RANGE:
            smoothed_ratio_x = CENTER_VALUE

        # 4) 언리얼에는 "스무딩된" X 비율만 전송 (변화가 일정 이상일 때만)
        if last_sent_ratio_x is None or abs(smoothed_ratio_x - last_sent_ratio_x) > SEND_THRESHOLD:
            osc.send_message("/gaze/x", float(smoothed_ratio_x))
            last_sent_ratio_x = smoothed_ratio_x

        # 5) 디버그용 픽셀 좌표
        gaze_px = int(smoothed_ratio_x * w)
        gaze_py = int(smoothed_ratio_y * h)

        smoothed_px = ema_update(smoothed_px, gaze_px, SMOOTH_ALPHA)
        smoothed_py = ema_update(smoothed_py, gaze_py, SMOOTH_ALPHA)

        # 디버그 표시 (얼굴 메쉬)
        if DRAW_DEBUG:
            mp_drawing.draw_landmarks(
                frame, results.multi_face_landmarks[0],
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=(80, 255, 80),
                    thickness=1,
                    circle_radius=0
                )
            )

    # =========================
    # 3개의 세로 칸 (가운데 넓게) + 현재 시선이 들어간 칸 판단
    # =========================
    active_zone = None

    # 픽셀 기준 경계 계산
    left_end_x    = int(LEFT_END_RATIO    * w)
    right_start_x = int(RIGHT_START_RATIO * w)

    # 왼쪽 존 (index 0)
    x0, x1 = 0, left_end_x
    color = (120, 120, 120)
    if smoothed_px is not None and x0 <= smoothed_px < x1:
        active_zone = 0
        color = (0, 200, 255)
    cv2.rectangle(frame, (x0, 0), (x1, h), color, 2)
    cv2.putText(frame, "A", (x0 + 10, 40), FONT, 1.1, color, 2, cv2.LINE_AA)

    # 가운데 존 (index 1)
    x0, x1 = left_end_x, right_start_x
    color = (120, 120, 120)
    if smoothed_px is not None and x0 <= smoothed_px < x1:
        active_zone = 1
        color = (0, 200, 255)
    cv2.rectangle(frame, (x0, 0), (x1, h), color, 2)
    cv2.putText(frame, "B", (x0 + 10, 40), FONT, 1.1, color, 2, cv2.LINE_AA)

    # 오른쪽 존 (index 2)
    x0, x1 = right_start_x, w
    color = (120, 120, 120)
    if smoothed_px is not None and x0 <= smoothed_px < x1:
        active_zone = 2
        color = (0, 200, 255)
    cv2.rectangle(frame, (x0, 0), (x1, h), color, 2)
    cv2.putText(frame, "C", (x0 + 10, 40), FONT, 1.1, color, 2, cv2.LINE_AA)

    # 시선 포인트(스무딩 결과) 그리기
    if smoothed_px is not None and smoothed_py is not None:
        cv2.circle(frame, (int(smoothed_px), int(smoothed_py)), 8, (0, 255, 0), -1)
        cv2.putText(
            frame,
            f"({int(smoothed_px)}, {int(smoothed_py)})",
            (10, h - 10),
            FONT, 0.7, (0, 255, 0), 2, cv2.LINE_AA
        )

    # 발 센서 상태 텍스트 (디버그용)
    cv2.putText(
        frame,
        f"L:{sensor_data['left']}  R:{sensor_data['right']}  (Last:{sensor_data['last']})",
        (10, 70),
        FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA
    )

    # 존 변경 이벤트 훅
    if active_zone is not None and active_zone != prev_zone:
        on_zone_change(active_zone)
        prev_zone = active_zone

    cv2.imshow("Eye+Foot Tracking - 3 Zones (Center Wide)", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
