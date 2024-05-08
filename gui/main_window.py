import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QAction
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from train_window import TrainWindow
from detect_window import DetectWindow
from data_window import DataWindow
import sys

class MainWindow(QMainWindow):
    def setUI(self):
        self.setWindowTitle('체크메이트-메인')
        self.resize(800, 600)
        self.center_window()
        font_id = QFontDatabase.addApplicationFont("SUITE-SemiBold.ttf")  
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # 버튼 추가
        self.button_data = QPushButton('데이터 관리', self)
        self.button_data.clicked.connect(self.open_data_window)
        self.set_button_style(self.button_data)

        self.button_train = QPushButton('모델 훈련', self)
        self.button_train.clicked.connect(self.open_train_window)
        self.set_button_style(self.button_train)

        self.button_detect = QPushButton('불량 탐지', self)
        self.button_detect.clicked.connect(self.open_detect_window)
        self.set_button_style(self.button_detect)

        # 수직 레이아웃 생성 및 버튼 추가
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_data)  
        self.button_layout.addWidget(self.button_train)
        self.button_layout.addWidget(self.button_detect)
    
    def __init__(self):
        super().__init__()
        self.setUI()
        # 필요한 종속성 설치
        command = "pip install -r yolov5/requirements.txt"
        try:
            subprocess.run(command, shell=True)
            print("필수 요소가 준비되었습니다...")
        except Exception as e:
            print("에러:", e)
        self.train_window = None
        self.data_window = None
        self.detect_window = None
        # 제목 레이블 및 사용자 정의 폰트 추가
        title_label = QLabel('체크메이트', self)
        title_font = QFont(self.font_family)
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # 수평 레이아웃 생성 및 버튼 레이아웃과 타이틀 레이블 추가
        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.button_layout)  # 버튼 레이아웃 추가
        hbox_layout.addWidget(title_label)
        hbox_layout.addStretch(1)  # 타이틀 레이블을 오른쪽으로 밀어냄

        # 중앙 위젯 생성
        central_widget = QWidget()
        central_widget.setLayout(hbox_layout)
        self.setCentralWidget(central_widget)

        # 중앙 위젯 생성
        central_widget = QWidget()
        central_widget.setLayout(hbox_layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        # 현재 화면의 가운데 좌표 계산
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2

        # 윈도우의 가운데 좌표 설정
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)

    def open_data_window(self):
        self.data_window = DataWindow(self)
        self.data_window.show()

    def open_train_window(self):
        self.train_window = TrainWindow(self)
        self.train_window.show()

    def open_detect_window(self):
        self.detect_window = DetectWindow(self)
        self.detect_window.show()

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: black;
                font-size: 16px;
                text-align: left;
                padding-left: 15px;  /* 왼쪽 여백 설정 */
                padding-right: 15px; /* 오른쪽 여백 설정 */
                font-family: "SUITE";
                width: 100px;
                height: 80px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);  /* 마우스 호버 시 배경색 변경 */
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.3);  /* 클릭 시 배경색 변경 */
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
