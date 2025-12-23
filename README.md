# ORDA-stepper-immersive-healthcare

# 🏔️ ORDA (오르다) - Immersive Healthcare 

> **"Step into the Virtual World."**
> 스텝퍼 운동에 AI 시선 추적 기술을 더한 **실감형 헬스케어 플랫폼**입니다.

<img src="https://github.com/user-attachments/assets/120b9b2f-2965-4e71-a24b-1742098aca6a" width="300">



## 📅 Project Overview
* **Project** Name: ORDA (오르다)
* **Type:** Capstone Design Project
* **Engine:** Unreal Engine 5.x
* **Hardware:** Stepper Machine, Arduino, Webcam, Headset

---
## 🎥 Project Demo
👉 **[YouTube 소개 영상(Click Here)](https://www.youtube.com/watch?v=dGxID1m1O6o)**

---
## 🌟 Expected Impact (기대 효과)
1. **Gamification of Exercise:** 지루한 반복 운동인 스텝퍼에 게임 요소를 도입하여 지속적인 운동 동기를 부여합니다.
2. **Immersive Experience:** 단순한 영상 시청을 넘어,사용자의 움직임에 반응하는 인터랙티브 콘텐츠로 몰입감을 극대화합니다.
3. **Data-Driven Health:** 실시간 운동 데이터(심박수, 속도, 걸음수 등)를 시각화하여 체계적인 운동을 도와줍니다.


---
## 💡 Key Features (핵심 기능)

### 1. 🏃‍♂️ Interactive Stepping System
* **실시간 동기화:** 사용자가 스텝퍼를 밟는 속도와 리듬이 가상 캐릭터의 움직임(Animation)에 즉각 반영됩니다.
* **센서 연동:** 초음파 센서(HC-SR04)와 아두이노를 활용하여 정밀한 발판 움직임을 감지합니다.

### 2. 👀 AI Gaze Tracking (시선 추적)
* **(Python)**: MediaPipe 기반의 AI 비전 시스템이 사용자의 눈동자를 실시간으로 추적합니다.
* **Head Tracking**: 사용자가 바라보는 방향으로 카메라 시점이 자연스럽게 회전하여, 주변 전경을 감상할 수 있습니다.

### 3. 🌏 Dual Theme Maps
* **Mountain (힐링)**: 폭포 소리와 자연의 소리가 어우러진 공간 음향(Spatial Audio) 적용.
* **The Great Wall (경쟁)**: 벚꽃이 흩날리는 만리장성에서 가상인물과 레이싱 경쟁을 펼치는 요소 적용.

### 4. 📊 Health Data Visualization
* 운동 중 심박수, 이동 속도, 걸음 수, 소요 시간을 직관적인 UI로 제공합니다.
* 1인칭(First-Person) 및 3인칭(Third-Person) 시점 전환을 지원합니다.

---
## 🛠️ System Architecture (시스템 구성)

### 📂 Arduino
* **File:** `Arduino/Sensor_Controller.ino`
* **Role:** 하드웨어 센싱
* 스텝퍼의 물리적 움직임을 디지털 신호로 변환, 시리얼 통신을 통해 PC로 전송합니다.

### 📂 Python_AI
* **File:** `Python_AI/Gaze_Tracking.py`
* **Role:** 데이터 및 좌표 연산
* 아두이노의 신호 수신 + 웹캠 시선 데이터 분석 → **OSC 프로토콜**을 통해 언리얼 엔진으로 통합 데이터 전송.

### 📂 Unreal_Project
* **Role:** 메인 콘텐츠 구동
* Nanite와 Lumen을 활용한 사실적인 그래픽 구현.

---
## 🚀 How to Run

1. **Hardware Connection:**
   - 아두이노와 PC를 USB로 연결합니다.
   - `Arduino/Sensor_Controller.ino`를 업로드합니다.

2. **Middleware Start:**
   - 파이썬 라이브러리를 설치합니다: `pip install pyserial python-osc opencv-python mediapipe`
   - 미들웨어 서버를 실행합니다: `python Python_AI/Gaze_Tracking.py`
   
3. **Unreal Start / Guide**
   - Unreal 프로젝트는 용량 문제로 GitHub에 전체 포함하지 않았습니다.
   - 대신 블루프린트 구조/실행 흐름/캡처 자료를 `guide/` 폴더에 정리했습니다.
   - 핵심 문서: `guide/blueprint_notes.md`

---
## 📚 References & Assets
* **Unreal Engine Marketplace:** Nature Package, Character Animations
* **Open Source Libraries:**
  * [MediaPipe](https://google.github.io/mediapipe/) (Gaze Tracking)
  * [Python-OSC](https://pypi.org/project/python-osc/) (Communication)
* **Hardware:** Arduino Uno, HC-SR04 Datasheet

---
## 👥 Team Members

| Name | Part (Main Task) | GitHub |
|:---:|:---|:---:|
| <sub>**하태윤**</sub> | <sub>System Architecture</sub> | <sub>[@gkxodbs011-aks](https://github.com/gkxodbs011-aks)</sub> |
| <sub>**황상준**</sub> | <sub>Hardware & Sensor Integration</sub> | <sub>[@kevinsj7878-png](https://github.com/kevinsj7878-png)</sub> |
| <sub>**이창규**</sub> | <sub>Unreal Logic & Interaction</sub> | <sub>[@bo0sik](https://github.com/bo0sik)</sub> |
| <sub>**김종민**</sub> | <sub>Level Design & Environment Art</sub> | <sub>[@couter0139](https://github.com/couter0139)</sub> |
| <sub>**김명진**</sub> | <sub>UI/UX & Sound Design</sub> | <sub>[@willkh200](https://github.com/willkh200)</sub> |
  
