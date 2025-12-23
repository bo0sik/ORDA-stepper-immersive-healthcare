# Unreal Blueprint Notes (BP_Arduino + BP_ThirdPersonCharacter)

이 문서는 본 프로젝트에서 **Arduino(스텝퍼) + Python(시선/센서 브릿지) → OSC → Unreal Engine**으로 입력을 받아
**캐릭터 이동 / 카메라 회전 / HUD 갱신**을 수행하는 블루프린트 구조를 설명합니다.

---

## 1. Blueprint 구성 개요

### 1) BP_Arduino (OSC 수신 전용 BP)
- 역할: OSC 메시지를 수신하고, 주소별로 값을 분기 처리(Dispatch)
- 출력: Stepper 이벤트(`/sensor/left_up`, `/sensor/right_up`) 및 시선 값(`/gaze/x`)을
  `BP_ThirdPersonCharacter`로 전달

### 2) BP_ThirdPersonCharacter (플레이어 캐릭터)
- 역할:
  - Stepper 입력 기반 전진/속도 반영
  - Gaze(시선/머리 방향) 기반 카메라 회전
  - HUD(Speed/HeartRate/Steps 등) 갱신을 위한 변수 관리

### 3) UI Widgets
- Start UI → Map Select UI → HUD 순서로 전환
- Map 2개(Mountain / Great Wall) 중 선택하여 레벨 진입
- 레벨 진입 시 HUD 표시

---

## 2. OSC 입력 스펙

Python에서 Unreal로 전송되는 주요 OSC 주소는 다음과 같습니다.

### 2.1 Stepper Events
- `/sensor/left_up`  : int(1)
- `/sensor/right_up` : int(1)

### 2.2 Gaze (Camera Direction)
- `/gaze/x` : float(0.0 ~ 1.0)
  - 좌우 시선 비율(정규화)
  - Unreal에서 카메라 Yaw(좌/우 회전) 보정값으로 매핑

(옵션)
- `/gaze/zone` : int(0/1/2)
- `/gaze/zone_label` : string(A/B/C)

---

## 3. BP_Arduino 구현(수신/분기)

### 3.1 OSC 수신 설정
- OSC 플러그인 활성화
- 수신 포트: **10000**
- (로컬 기준) Python이 `127.0.0.1:10000`으로 메시지 전송

### 3.2 주소 분기(Dispatch)
BP_Arduino는 수신된 Address Pattern을 기준으로 분기합니다.

- Address == `/sensor/left_up`  → Left Step 이벤트 발생
- Address == `/sensor/right_up` → Right Step 이벤트 발생
- Address == `/gaze/x`          → GazeX(float) 변수 갱신 후 전달

### 3.3 BP_ThirdPersonCharacter로 전달
(대표 방식)
- BP_Arduino BeginPlay:
  - `Get Player Character` → `Cast to BP_ThirdPersonCharacter` → 변수로 저장
- 이벤트 발생 시:
  - Left Step  → `HandleLeftStep()`
  - Right Step → `HandleRightStep()`
  - GazeX      → `SetGazeX(GazeX)`

---

## 4. BP_ThirdPersonCharacter 구현(이동/카메라/HUD)

### 4.1 Stepper 입력으로 전진(속도 반영)
- Steps(걸음수) 증가
- 스텝 간격을 이용해 속도 추정(선택)
- 전진 속도/이동량을 보정(Clamp + Interp 권장)
- 구현 방식 예시:
  - CharacterMovement `Max Walk Speed` 업데이트
  - 또는 `Add Movement Input(Forward)` 스케일 조절

### 4.2 GazeX로 카메라 Yaw 회전
- `Centered = (GazeX - 0.5)` → -0.5 ~ +0.5
- `YawOffset = Centered * YawScale` (예: 30~60도)
- SpringArm/Camera Yaw에 적용
- Deadzone + Interp로 부드럽게(권장)

### 4.3 HUD 갱신
- Speed / HeartRate / Steps / Time 등 변수를 갱신
- Widget이 바인딩 또는 이벤트로 표시

