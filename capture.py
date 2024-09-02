import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
import pyautogui
import time
import random
from pynput import mouse

page = 30   # 찍을 페이지 수
index = 0   # 이미지 파일명 인덱스
picture_size = [641,123,1407,1105] # 왼쪽 상단 좌표 , 오른쪽 하단 좌표

msg = "버튼에 마우스를 올리면 설명이 나옵니다."

def replace_start_point(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        print('입력받은 좌표 : ', (x, y))
        picture_size[0] = x
        picture_size[1] = y
        print(picture_size)
    return False

def replace_end_point(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        print('입력받은 좌표 : ', (x, y))
        picture_size[2] = x
        picture_size[3] = y
        print(picture_size)
    return False

def calculate_midpoint(picture_size):
    # 좌표 분리
    x1, y1 = picture_size[0], picture_size[1]  # 왼쪽 상단
    x2, y2 = picture_size[2], picture_size[3]  # 오른쪽 하단

    # 중간 지점 계산
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    return (mid_x, mid_y)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_mouse_position)
        self.timer.start(100) 

    def initUI(self):
        self.setWindowTitle('스크린샷 매크로')
        self.statusBar().showMessage(msg)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        self.page_input_label = QLabel('Page:', self)
        self.page_input_label.move(30,50)
        self.page_input_field = QLineEdit(self)
        self.page_input_field.move(120,50)
        self.page_input_field.setText(str(page))

        self.index_input_label = QLabel('Index:', self)
        self.index_input_label.move(30,100)
        self.index_input_field = QLineEdit(self)
        self.index_input_field.move(120,100)
        self.index_input_field.setText(str(index))

        self.x1_input_label = QLabel('왼쪽 상단 X', self)
        self.x1_input_label.move(30, 150)
        self.x1_input_field = QLineEdit(self)
        self.x1_input_field.move(120, 150)
        self.x1_input_field.setText(str(picture_size[0]))

        self.y1_input_label = QLabel('왼쪽 상단 Y', self)
        self.y1_input_label.move(30, 200)
        self.y1_input_field = QLineEdit(self)
        self.y1_input_field.move(120, 200)
        self.y1_input_field.setText(str(picture_size[1]))

        self.x2_input_label = QLabel('오른쪽 하단 X', self)
        self.x2_input_label.move(30, 250)
        self.x2_input_field = QLineEdit(self)
        self.x2_input_field.move(120, 250)
        self.x2_input_field.setText(str(picture_size[2]))

        self.y2_input_label = QLabel('오른쪽 하단 Y', self)
        self.y2_input_label.move(30, 300)
        self.y2_input_field = QLineEdit(self)
        self.y2_input_field.move(120, 300)
        self.y2_input_field.setText(str(picture_size[3]))

        self.btn_start_point = QPushButton('왼쪽 상단 좌표 저장', self)
        self.btn_start_point.setToolTip('캡쳐할 부분의 왼쪽 상단 꼭지점에 마우스를 두고 클릭합니다.')
        self.btn_start_point.move(250, 150)
        self.btn_start_point.resize(self.btn_start_point.sizeHint())
        self.btn_start_point.clicked.connect(self.event_start_point)

        self.btn_end_point = QPushButton('오른쪽 하단 좌표 저장', self)
        self.btn_end_point.setToolTip('캡쳐할 부분의 오른쪽 하단 꼭지점에 마우스를 두고 클릭합니다.')
        self.btn_end_point.move(250, 250)
        self.btn_end_point.resize(self.btn_end_point.sizeHint())
        self.btn_end_point.clicked.connect(self.event_end_point)

        btn_run = QPushButton('실행하기', self)
        btn_run.setToolTip('다른 프로그램이 이미지를 가리지 않도록 해주세요.')
        btn_run.move(30, 350)
        btn_run.resize(btn_run.sizeHint()) 
        btn_run.clicked.connect(self.capture)
        self.setGeometry(400,400,500,500)
        self.show()

    def event_start_point(self):
        with mouse.Listener(on_click=replace_start_point) as listener:
            listener.join()
            self.x1_input_field.setText(str(picture_size[0]))
            self.y1_input_field.setText(str(picture_size[1]))
            msg = "왼쪽 상단 좌표 : (%s, %s)"%(picture_size[0], picture_size[1])
            self.statusBar().showMessage(msg)

    def event_end_point(self):
        with mouse.Listener(on_click=replace_end_point) as listener:
            listener.join()
            self.x2_input_field.setText(str(picture_size[2]))
            self.y2_input_field.setText(str(picture_size[3]))
            msg = "오른쪽 하단 좌표 : (%s, %s)"%(picture_size[2], picture_size[3])
            self.statusBar().showMessage(msg)

    def update_mouse_position(self):
        # 마우스 커서 위치 얻기
        cursor_pos = QCursor.pos()
        self.statusBar().showMessage("마우스 위치: (%d, %d)" % (cursor_pos.x(), cursor_pos.y()))

    def capture(self):
        global index, page, picture_size
        index = int(self.index_input_field.text())
        page = int(self.page_input_field.text())
        x1 = int(self.x1_input_field.text())
        y1 = int(self.y1_input_field.text())
        x2 = int(self.x2_input_field.text())
        y2 = int(self.y2_input_field.text())
        picture_size = [x1, y1, x2, y2]
        midpoint = [calculate_midpoint(picture_size)]
        pyautogui.click(*midpoint)
        time.sleep(0.8)
        pyautogui.click(*midpoint)
        time.sleep(0.8)
        for i in range(page):
            if len(picture_size) >= 4:
                pyautogui.screenshot("%s.png" % index, region=(picture_size[0], picture_size[1],
                    picture_size[2]-picture_size[0],picture_size[3]-picture_size[1]))
                index += 1
            pyautogui.press('right')
            time.sleep(random.uniform(0.8, 1.2))
        self.index_input_field.setText(str(index))
        msg = "이미지 캡쳐 완료"
        print(msg)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())