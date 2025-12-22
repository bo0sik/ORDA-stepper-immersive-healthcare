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

### 📂 (Arduino)
* Role: 하드웨어 센싱
* 스텝퍼의 물리적 움직임을 디지털 신호로 변환, 시리얼 통신을 통해 PC로 전송합니다.

### 📂 (Python)
* Role: 데이터 중계 및 AI 연산
* 아두이노의 신호 수신 + 웹캠 시선 데이터 분석 → OSC 프로토콜을 통해 언리얼 엔진으로 통합 데이터 전송.

### 📂 Unreal Engine 5
* Role: 메인 콘텐츠 구동
* 나나이트(Nanite) 및 루멘(Lumen) 기술을 활용한 고품질 그래픽 렌더링.
  
