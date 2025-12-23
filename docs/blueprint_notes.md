## 🖼️ Demo 

- Start UI
- Map Select UI (Mountain / Great Wall)
- HUD (Speed / HeartRate / Steps)
- Mountain: Waterfall 접근 장면(사운드 강조)
- Great Wall: NPC(국기/닉네임) 경쟁 장면
- Gaze/Head Tracking 카메라 회전 비교 (Before / After)

---
## 📡 OSC Message Specification
Python 미들웨어가 Unreal로 전송하는 OSC 주소는 다음과 같습니다.

### Stepper
- `/sensor/left_up`  : `int(1)`
- `/sensor/right_up` : `int(1)`

### Gaze / Camera
- `/gaze/x` : `float(0.0 ~ 1.0)`  (좌우 시선 비율 값)

(Option)
- `/gaze/zone` : `int(0/1/2)`
- `/gaze/zone_label` : `string(A/B/C)`

Default Target:
- IP: `127.0.0.1`
- Port: `10000`

---
## 🎮 Unreal Project (Large Files Notice)

대신 아래 자료로 핵심 로직이 재현 가능하도록 정리했습니다.
- `docs/blueprint_notes.md` : `BP_Arduino`(OSC 수신) ↔ `BP_ThirdPersonCharacter`(이동/카메라/HUD) 연결 구조
- `docs/USER_MANUAL.pdf` : 작품 체험 안내 매뉴얼(사진 포함)
- `screenshots/` : UI/맵/HUD/카메라 회전/NPC 등 실행 캡처

---
## 🧯 Troubleshooting
### COM Port / Serial
- PC마다 COM 포트가 달라질 수 있습니다.
  Windows 장치 관리자에서 Arduino COM 번호 확인 후 Python 코드의 `SER_PORT` 값을 수정하세요.

### OSC Port
- Unreal 수신 포트(기본 10000)가 다른 프로그램과 충돌하면 변경이 필요합니다.
  Python과 Unreal의 포트를 동일하게 맞추세요.

### Dependencies
- `mediapipe`, `opencv-python` 설치가 실패하면 Python 버전(3.10~3.11 권장) 확인 후 재설치하세요.

