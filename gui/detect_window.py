from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import sys


class ImageRecognitionDialog(QDialog):
    # 시그널 선언
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Recognition')

        # 파일 업로드 버튼 생성
        upload_button = QPushButton("Upload", self)
        upload_button.clicked.connect(self.upload_image)
          
        # 선택된 파일의 경로를 표시할 QLabel 생성
        self.file_path_label = QLabel(self)
        self.file_path_label.setWordWrap(True)

        # 수직 레이아웃 생성하여 위젯 추가
        layout = QVBoxLayout()
        layout.addWidget(upload_button)
        layout.addWidget(self.file_path_label, alignment=Qt.AlignCenter)

        # 다이얼로그에 레이아웃 설정
        self.setLayout(layout)

        # 탐지 버튼 생성
        self.detect_button = QPushButton("Detect", self)
        self.detect_button.clicked.connect(self.detect_objects)
        self.detect_button.hide()

    def upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path_label.setText("Selected file: " + file_path)
            self.file_selected.emit(file_path)  # 파일 경로를 부모 다이얼로그로 전달하는 시그널 발생
            self.detect_button.show()  # 파일 선택 시 탐지 버튼을 표시함

    def detect_objects(self):
        # 탐지 버튼을 누르면 탐지 작업을 수행함
        file_path = self.file_path_label.text().replace("Selected file: ", "")
        self.file_selected.emit(file_path)


class DetectWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CheckMate - detect')

        # 윈도우 크기 설정
        self.resize(800, 600)

        # 윈도우를 화면 가운데에 위치시키기
        self.center_window()

        # 제목 레이블 생성
        title_label = QLabel('DETECT', self)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))

        # 홈 버튼 생성
        home_button = QPushButton(self)
        home_button.setIcon(QIcon("home.png"))  # 홈 아이콘 설정
        home_button.clicked.connect(self.go_home)  # 홈 버튼 클릭 시 go_home 메서드 호출
        home_button.setStyleSheet("border: none;")

        # 콤보박스 생성
        self.model_combo_box = QComboBox(self)
        self.model_combo_box.addItem("Model 1")
        self.model_combo_box.addItem("Model 2")
        self.model_combo_box.addItem("Model 3")

        # 이미지 인식 버튼 생성
        self.image_recognition_button = QPushButton("Image Recognition", self)
        self.image_recognition_button.clicked.connect(self.image_recognition)

        # 영상 인식 테스트 버튼 생성
        self.live_recognition_button = QPushButton("Test Live Video Recognition", self)
        self.live_recognition_button.clicked.connect(self.live_recognition)

        # 수직 레이아웃 생성하여 위젯 추가
        layout = QVBoxLayout()
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(home_button)
        layout.addWidget(self.model_combo_box, alignment=Qt.AlignCenter)
        layout.addStretch()  # 수직 방향으로 공간을 최대한 늘림
        layout.addWidget(self.image_recognition_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.live_recognition_button, alignment=Qt.AlignCenter)

        # 다이얼로그에 레이아웃 설정
        self.setLayout(layout)

        # 이미지 업로드 다이얼로그 생성
        self.image_dialog = ImageRecognitionDialog()
        self.image_dialog.file_selected.connect(self.detect)

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
        print("Detect Result")

    def closeEvent(self, event):
        # TrainWindow가 닫힐 때 위치와 크기 정보 저장
        self.last_position = self.pos()
        self.last_size = self.size()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DetectWindow()
    window.show()
    sys.exit(app.exec_())
