import subprocess
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon, QFont, QPixmap, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal
import sys, os


class ImageRecognitionDialog(QDialog):
    # 시그널 선언
    file_selected = pyqtSignal(str)
    detect_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.resize(400, 600)
        self.setWindowTitle('이미지 인식')

        # 파일 업로드 버튼 생성
        upload_button = QPushButton("업로드", self)
        upload_button.clicked.connect(self.upload_image)
          
        # 선택된 파일의 경로를 표시할 QLabel 생성
        self.file_path_label = QLabel(self)
        self.file_path_label.setWordWrap(True)

        # 이미지를 표시할 QLabel 생성
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)

        # 수직 레이아웃 생성하여 위젯 추가
        layout = QVBoxLayout()
        layout.addWidget(self.file_path_label, alignment=Qt.AlignCenter)
        layout.addWidget(upload_button)
        layout.addWidget(self.image_label)

        # 다이얼로그에 레이아웃 설정
        self.setLayout(layout)

        # 탐지 버튼 생성
        self.detect_button = QPushButton("탐지", self)
        self.detect_button.clicked.connect(self.detect_objects)
        self.detect_button.hide()        
        layout.addWidget(self.detect_button)

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path_label.setText("선택된 파일: " + file_path)
            self.file_selected.emit(file_path)  # 파일 경로를 부모 다이얼로그로 전달하는 시그널 발생
            
            # 이미지를 QLabel에 표시
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()

            self.detect_button.show()  # 파일 선택 시 탐지 버튼을 표시함

    def detect_objects(self):
        # 탐지 버튼을 누르면 탐지 작업을 수행함
        self.detect_requested.emit()
class DetectWindow(QDialog):
    def setUI(self, MainWindow):

        self.main_window = MainWindow
        self.setWindowTitle('체크메이트-불량 탐지')
        self.resize(800, 600)
        self.center_window()
        font_id = QFontDatabase.addApplicationFont("SUITE-SemiBold.ttf")  
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # 버튼 추가
        self.button_data = QPushButton('데이터 관리', self)
        self.button_data.clicked.connect(self.main_window.open_data_window)
        self.main_window.set_button_style(self.button_data)

        self.button_train = QPushButton('모델 훈련', self)
        self.button_train.clicked.connect(self.main_window.open_train_window)
        self.main_window.set_button_style(self.button_train)

        self.button_detect = QPushButton('불량 탐지', self)
        self.main_window.set_button_style(self.button_detect)

        # 수직 레이아웃 생성 및 버튼 추가
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_data)  
        self.button_layout.addWidget(self.button_train)
        self.button_layout.addWidget(self.button_detect)

    def __init__(self, MainWindow):
        super().__init__()
        self.setUI(MainWindow)
        # 제목 레이블 생성
        title_label = QLabel('불량 탐지', self)
        title_label.setFont(QFont(self.font_family, 20, QFont.Bold))

        # 홈 버튼 생성
        home_button = QPushButton(self)
        home_button.setIcon(QIcon("gui/home.png"))  # 홈 아이콘 설정
        home_button.clicked.connect(self.go_home)  # 홈 버튼 클릭 시 go_home 메서드 호출
        home_button.setStyleSheet("border: none;")        
        home_button.setToolTip("홈으로")

        # 콤보박스 생성
        self.model_combo_box = QComboBox(self)
        items_path = "data"
        items_dir = [d for d in os.listdir(items_path) if os.path.isdir(os.path.join(items_path, d))]
        self.model_combo_box.addItems(items_dir)

        # 이미지 인식 버튼 생성
        self.image_recognition_button = QPushButton("이미지 인식", self)
        self.image_recognition_button.clicked.connect(self.image_recognition)

        # 영상 인식 테스트 버튼 생성
        self.live_recognition_button = QPushButton("실시간 영상 인식", self)
        self.live_recognition_button.clicked.connect(self.live_recognition)

        # 수직 레이아웃 생성하여 위젯 추가
        layout = QVBoxLayout()
        layout.addWidget(home_button, alignment=Qt.AlignLeft)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.model_combo_box, alignment=Qt.AlignCenter)
        layout.addStretch()  # 수직 방향으로 공간을 최대한 늘림
        layout.addWidget(self.image_recognition_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.live_recognition_button, alignment=Qt.AlignCenter)

        # 다이얼로그에 레이아웃 설정
        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.button_layout)
        hbox_layout.addLayout(layout)
        self.setLayout(hbox_layout)

        # # 이미지 업로드 다이얼로그 생성
        self.image_dialog = ImageRecognitionDialog()
        self.image_dialog.detect_requested.connect(self.detect)

    def go_home(self):
        self.close()

    def center_window(self):
        # 현재 모니터의 가운데 좌표 계산
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2

        # 윈도우의 가운데 좌표 설정
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)

    def image_recognition(self):
        # 이미지 업로드 다이얼로그 표시
        self.image_dialog.exec_()

    def live_recognition(self):
        print("Testing live video recognition...")
    
    def detect(self):
        file_path = self.image_dialog.file_path_label.text().replace("선택된 파일: ", "")
        command = f"python ./yolov5/detect.py --weights ./yolov5/runs/train/{self.model_combo_box.currentText()}/weights/best.pt --conf 0.5 --source {file_path}"
        try:
            # shell 명령 실행
            subprocess.run(command, shell=True)
            print("Training model...")
        except Exception as e:
            print("Error:", e)

    def closeEvent(self, event):
        # TrainWindow가 닫힐 때 위치와 크기 정보 저장
        self.last_position = self.pos()
        self.last_size = self.size()
        super().closeEvent(event)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = DetectWindow()
#     window.show()
#     sys.exit(app.exec_())
