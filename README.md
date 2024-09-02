# 스크린샷 매크로

## 실행 방법

### python 3.12.5 버전 설치
- [Download Python | python.org](https://www.python.org/downloads/)
### 패키지 설치
- `pip install PyQt5 pyautogui pynput pillow`

### 실행
- `python capture.py`

## 사용법
![K-002](https://github.com/user-attachments/assets/43331375-bce1-406e-88ab-8c35da273e7b)

- `Page`에 캡쳐할 횟수 입력
- `Index`에 캡쳐 후 저장될 파일의 이름의 시작 인덱스 입력
  - e.g.) `Page`가 3, `Index`가 0이면 0.png, 1.png, 2.png 로 이미지가 저장된다.
- 캡쳐할 부분을 좌표로 저장
  - input 란에 직접 입력해도 되고, 좌표 저장 버튼을 클릭해 자동으로 입력할 수도 있다.
- `실행하기` 버튼을 클릭하면 캡쳐가 진행된다.
