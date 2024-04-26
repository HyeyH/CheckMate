from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout, QAction
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from train_window import TrainWindow
from detect_window import DetectWindow
from data_window import DataWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CheckMate - main')

        # 윈도우 크기 설정
        self.resize(800, 600)

        # 윈도우를 화면 가운데에 위치시키기
        self.center_window()

        # 툴바 생성
        self.toolbar = self.addToolBar('Main Toolbar')
        
        # 홈 액션 추가
        self.home_action = QAction(QIcon("home.png"), 'Home', self)
        self.home_action.triggered.connect(self.go_home)
        self.toolbar.addAction(self.home_action)

        # 제목 레이블 생성
        title_label = QLabel('CheckMate', self)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)

        # 버튼 생성

        
        self.button_data = QPushButton('DATA', self)
        self.button_data.setFixedSize(200, 100)
        self.button_data.clicked.connect(self.open_data_window)  # Connect clicked signal to open_train_window method

        self.button_train = QPushButton('TRAIN', self)
        self.button_train.setFixedSize(200, 100)
        self.button_train.clicked.connect(self.open_train_window)  # Connect clicked signal to open_train_window method

        self.button_detect = QPushButton('DETECT', self)
        self.button_detect.setFixedSize(200, 100)
        self.button_detect.clicked.connect(self.open_detect_window)  # Connect clicked signal to open_train_window method

        

        # 그리드 레이아웃 생성
        grid_layout = QGridLayout()
        grid_layout.addWidget(title_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)  # 제목 레이블 가운데 정렬
        
        grid_layout.addWidget(self.button_data, 1, 0, alignment=Qt.AlignCenter)  # 버튼 가운데 정렬
        grid_layout.addWidget(self.button_train, 1, 1, alignment=Qt.AlignCenter)  # 버튼 가운데 정렬
        grid_layout.addWidget(self.button_detect, 1, 2, alignment=Qt.AlignCenter)  # 버튼 가운데 정렬

        # 중앙 위젯 생성
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        # 현재 모니터의 가운데 좌표 계산
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
        self.hide()
        self.detect_window = DetectWindow()
        self.detect_window.exec()
        self.move(self.detect_window.last_position)
        self.resize(self.detect_window.last_size)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
