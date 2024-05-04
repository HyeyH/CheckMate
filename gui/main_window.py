import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QAction
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from train_window import TrainWindow
from detect_window import DetectWindow
from data_window import DataWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('체크메이트-메인')
        self.resize(800, 600)
        self.center_window()

        # 툴바 추가
        self.toolbar = self.addToolBar('Main Toolbar')

        # 홈 액션 추가
        self.home_action = QAction(QIcon("gui/home.png"), '홈', self)
        self.home_action.triggered.connect(self.go_home)
        self.toolbar.addAction(self.home_action)

        # 제목 레이블 및 사용자 정의 폰트 추가
        title_label = QLabel('체크메이트', self)
        font_id = QFontDatabase.addApplicationFont("SUITE-Regular.ttf")  # "path/to/SUITE-Regular.ttf"를 실제 파일 경로로 대체해주세요
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        title_font = QFont(font_family)
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)

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
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_data)  
        button_layout.addWidget(self.button_train)
        button_layout.addWidget(self.button_detect)

        # 수평 레이아웃 생성 및 타이틀 레이블과 버튼 레이아웃 추가
        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(button_layout)
        hbox_layout.addWidget(title_label)  

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

    def go_home(self):
        self.show()

    def open_data_window(self):
        self.hide()
        self.data_window = DataWindow()
        self.data_window.exec()
        self.move(self.data_window.last_position)
        self.resize(self.data_window.last_size)
        self.show()

    def open_train_window(self):
        self.hide()
        self.train_window = TrainWindow()
        self.train_window.exec()
        self.move(self.train_window.last_position)
        self.resize(self.train_window.last_size)
        self.show()

    def open_detect_window(self):
        self.hide()
        self.detect_window = DetectWindow()
        self.detect_window.exec()
        self.move(self.detect_window.last_position)
        self.resize(self.detect_window.last_size)
        self.show()

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: black;
                font-size: 16px;
                text-align: left;
                padding-left: 20px;  /* 왼쪽 여백 설정 */
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
