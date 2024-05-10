from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QFontMetrics, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
import sys, subprocess, os

class TrainWindow(QDialog):
    def setUI(self, MainWindow):
        
        self.main_window = MainWindow
        self.setWindowTitle('체크메이트-물품 훈련')
        self.resize(800, 600)
        self.center_window()
        font_id = QFontDatabase.addApplicationFont("SUITE-SemiBold.ttf")  
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # 버튼 추가
        self.button_data = QPushButton('데이터 관리', self)
        self.button_data.clicked.connect(self.main_window.open_data_window)
        self.main_window.set_button_style(self.button_data)

        self.button_train = QPushButton('모델 훈련', self)
        # self.button_train.clicked.connect(self.open_train_window)
        self.main_window.set_button_style(self.button_train)

        self.button_detect = QPushButton('불량 탐지', self)
        self.button_detect.clicked.connect(self.main_window.open_detect_window)
        self.main_window.set_button_style(self.button_detect)

        # 수직 레이아웃 생성 및 버튼 추가
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_data)  
        self.button_layout.addWidget(self.button_train)
        self.button_layout.addWidget(self.button_detect)
        
    def __init__(self, MainWindow):
        super().__init__()
        self.setUI(MainWindow)

        # 버튼 생성
        home_button = QPushButton(self)
        home_button.setIcon(QIcon("gui/home.png"))  # 그림 파일 경로를 지정하여 아이콘 설정
        home_button.clicked.connect(self.go_home)  # 윈도우를 닫는 버튼
        home_button.setStyleSheet("border: none;")        
        home_button.setToolTip("홈으로")

        # 제목 레이블 생성
        self.title_label = QLabel('모델 훈련')
        self.title_font = QFont(self.font_family, 20, QFont.Bold)
        self.title_label.setFont(self.title_font)

        self.subtitle_label = QLabel('체크메이트 사용을 위한 물품 훈련을 위한 창입니다.\n해당 창에서 데이터셋을 이용하여 모델을 훈련 시킬 수 있습니다.')
        self.subtitle_font = QFont(self.font_family, 10, QFont.Normal)
        self.subtitle_label.setFont(self.subtitle_font)

        # 콤보박스 생성
        self.model_combo_box = QComboBox()
        items_path = "data"
        items_dir = [d for d in os.listdir(items_path) if os.path.isdir(os.path.join(items_path, d))]
        self.model_combo_box.addItems(items_dir)
        self.selected_model_name = self.model_combo_box.currentText()

        # 모델 훈련 버튼 생성
        self.yolo_train_button = QPushButton('YOLO 훈련')
        self.yolo_train_button.clicked.connect(self.train_model)

        # 모델 삭제 버튼 생성
        self.autoencoder_train_button = QPushButton('오토인코더 훈련')
        self.autoencoder_train_button.clicked.connect(self.delete_model)

        # 모델 내보내기 버튼 생성
        self.export_model_button = QPushButton('모델 내보내기')
        self.export_model_button.clicked.connect(self.export_model)

        # 모델 불러오기 버튼 생성
        self.load_model_button = QPushButton('모델 불러오기')
        self.load_model_button.clicked.connect(self.load_model)

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.addWidget(home_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.model_combo_box)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yolo_train_button)
        button_layout.addWidget(self.autoencoder_train_button)
        main_layout.addLayout(button_layout)

        # 모델 내보내기 및 불러오기 버튼 추가
        main_layout.addWidget(self.export_model_button)
        main_layout.addWidget(self.load_model_button)
        
        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.button_layout)
        hbox_layout.addLayout(main_layout)
        self.setLayout(hbox_layout)

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
    def train_model(self):    
        # 명령 문자열
        command = f"python yolov5/train.py --data yolov5/{self.selected_model_name}/data.yaml --cfg yolov5/models/yolov5s.yaml --weights yolov5s.pt --batch 8 --epochs 100 --name {self.selected_model_name}"
        try:
            # shell 명령 실행
            subprocess.run(command, shell=True)
            print("Training model...")
        except Exception as e:
            print("Error:", e)

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
        self.main_window.show()
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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = TrainWindow(MainWindow=)
#     window.show()
#     sys.exit(app.exec_())
