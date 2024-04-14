from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox, QLineEdit, QGridLayout, QWidget, QAction, QToolBar, QFileDialog
from PyQt5.QtGui import QFont, QFontMetrics, QIcon
from PyQt5.QtCore import Qt
import sys


class TrainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CheckMate - train')

        # 윈도우 크기 설정
        self.resize(800, 600)

        # 윈도우를 화면 가운데에 위치시키기
        self.center_window()

        # 버튼 생성
        home_button = QPushButton(self)
        home_button.setIcon(QIcon("home.png"))  # 그림 파일 경로를 지정하여 아이콘 설정
        home_button.clicked.connect(self.close)  # 윈도우를 닫는 버튼
        home_button.setStyleSheet("border: none;")

        # 제목 레이블 생성
        self.title_label = QLabel('TRAIN')
        self.title_font = QFont("Arial", 20, QFont.Bold)
        self.title_label.setFont(self.title_font)

        # 콤보박스 생성
        self.model_combo_box = QComboBox()
        self.model_combo_box.addItems(['Lipstick', 'Milk', 'Figure', 'Logo'])

        # 모델 훈련 버튼 생성
        self.train_model_button = QPushButton('모델 훈련')
        self.train_model_button.clicked.connect(self.train_model)

        # 모델 삭제 버튼 생성
        self.delete_model_button = QPushButton('모델 삭제')
        self.delete_model_button.clicked.connect(self.delete_model)

        # 모델 내보내기 버튼 생성
        self.export_model_button = QPushButton('모델 내보내기')
        self.export_model_button.clicked.connect(self.export_model)

        # 모델 불러오기 버튼 생성
        self.load_model_button = QPushButton('모델 불러오기')
        self.load_model_button.clicked.connect(self.load_model)



        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(home_button, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.model_combo_box)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.train_model_button)
        button_layout.addWidget(self.delete_model_button)
        main_layout.addLayout(button_layout)

        # 모델 내보내기 및 불러오기 버튼 추가
        main_layout.addWidget(self.export_model_button)
        main_layout.addWidget(self.load_model_button)

        self.setLayout(main_layout)

    def train_model(self):
        # 모델 훈련 버튼 클릭 시 동작
        print("Training model...")

    def delete_model(self):
        # 모델 삭제 버튼 클릭 시 동작
        print("Deleting model...")

    def export_model(self):
        # 모델 내보내기 버튼 클릭 시 동작
        print("Exporting model...")

    def load_model(self):
        # 모델 불러오기 버튼 클릭 시 동작
        print("Loading model...")

    def go_home(self):
        self.close()
    
    def closeEvent(self, event):
        # TrainWindow가 닫힐 때 위치와 크기 정보 저장
        self.last_position = self.pos()
        self.last_size = self.size()
        super().closeEvent(event)

    def center_window(self):
        # 현재 모니터의 가운데 좌표 계산
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2

        # 윈도우의 가운데 좌표 설정
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TrainWindow()
    window.show()
    sys.exit(app.exec_())
