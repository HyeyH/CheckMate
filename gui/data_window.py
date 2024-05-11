from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTreeView, QFileSystemModel, QMessageBox, QFileDialog, QDialogButtonBox, QRadioButton, QTextEdit
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QDir
import sys, os
import subprocess
import shutil
import yaml


class DataWindow(QDialog):
    def setUI(self, MainWindow):
        self.main_window = MainWindow
        self.setWindowTitle('체크메이트-데이터 관리')
        self.resize(800, 600)
        self.center_window()
        font_id = QFontDatabase.addApplicationFont("SUITE-SemiBold.ttf")  
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setFont(QFont(self.font_family))
        
        # 버튼 추가
        self.button_data = QPushButton('데이터 관리', self)
        self.main_window.set_button_style(self.button_data)

        self.button_train = QPushButton('모델 훈련', self)
        self.button_train.clicked.connect(self.main_window.open_train_window)
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
        self.title_label = QLabel('데이터')
        self.title_font = QFont(self.font_family, 20, QFont.Bold)


        # 부제목 레이블 생성
        self.subtitle_label = QLabel('체크메이트 사용을 위한 데이터셋 관리를 위한 창입니다.\n해당 창에서 추가한 데이터셋과 라벨링한 데이터셋을 통해 체크메이트를 학습 시킬 수 있습니다.')
        self.subtitle_font = QFont(self.font_family, 10, QFont.Normal)


        self.tree_view = QTreeView()
        self.data_model = QFileSystemModel()

        # 데이터 디렉토리 경로 설정
        data_directory = "../data"
        root_path = QDir.rootPath()
        data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), data_directory))
        self.data_model.setRootPath(root_path)
        self.tree_view.setModel(self.data_model)
        self.tree_view.setRootIndex(self.data_model.index(data_directory))
        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)

        self.add_button = QPushButton('데이터셋 추가')
        self.add_button.clicked.connect(self.open_add_data)
        self.add_button.setToolTip("물품에 대한 새로운 이미지를 추가합니다.")

        self.label_button = QPushButton('데이터셋 라벨링')
        self.label_button.clicked.connect(self.open_label_data)
        self.label_button.setToolTip("추가한 데이터에 대한 라벨링을 진행합니다.")

        self.ratio_button = QPushButton('데이터셋 비율 지정')
        self.ratio_button.clicked.connect(self.open_ratio_data)
        self.ratio_button.setToolTip("훈련을 위한 데이터셋 비율을 지정합니다.")

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.addWidget(home_button, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.subtitle_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.label_button)
        main_layout.addWidget(self.ratio_button)

        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.button_layout)
        hbox_layout.addLayout(main_layout)
        self.setLayout(hbox_layout)

    def open_ratio_data(self):
        None
        
    def save_yaml_file(self, file_path, data):
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

    def load_yaml_file(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    def open_label_data(self):
        dialog = QDialog()
        dialog.resize(400, 500)
        
        layout = QVBoxLayout()
        label = QLabel("데이터를 라벨링할 물품의 이름을 하나만 입력하세요. 예) eraser")
        layout.addWidget(label)
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        button_ok = QPushButton("확인")

        def on_button_ok_clicked():
            item_name = text_edit.toPlainText().strip()  # text_edit의 텍스트를 가져옴 (양쪽 공백 제거)
            if not item_name:
                QMessageBox.warning(self, "경고", "물품명을 입력하세요.")
                return
            else:
                directory = os.path.join("data/"+item_name, 'labels')
                os.makedirs(directory, exist_ok=True)  # 디렉터리가 이미 있으면 오류를 발생시키지 않음
                QMessageBox.information(self, "완료", f"해당 물품명 디렉터리에 labels 폴더가 생성되었습니다.\n경로: {directory}")
                dialog.close()
        button_ok.clicked.connect(on_button_ok_clicked)
        layout.addWidget(button_ok)
        dialog.setLayout(layout)
        dialog.exec_()
        
        # exe_path = os.path.join("labelImg", 'labelImg.py')
        # if os.path.exists(exe_path) and os.access(exe_path, os.X_OK):
        #     process = subprocess.Popen(['python', exe_path])
        #     process.wait()
        # else:
        #     QMessageBox.warning(self, "Error", "데이터 라벨링을 진행할 수 없습니다.")
                
        exe_path = os.path.join("labelImg", 'labelImg.exe')
        if os.path.exists(exe_path) and exe_path.endswith(".exe"):
            # labelImg.exe 파일이 존재하고 확장자가 .exe인 경우 실행
            process = subprocess.Popen([exe_path])
            process.wait()
        else:
            QMessageBox.warning(self, "Error", "데이터 라벨링을 진행할 수 없습니다.")
        

    def open_add_data(self):
        dialog = QDialog(self)
        dialog.setFont(QFont(self.font_family))
        dialog.setWindowTitle("데이터 추가")
        dialog.resize(500, 500)
        item_label = QLabel("추가할 데이터의 이름을 영문으로 작성해 주세요. 예) eraser, milk")

        self.item_name = QTextEdit()  
        self.item_name.setFixedHeight(30)
        item_layout = QVBoxLayout()
        item_layout.addWidget(item_label)
        item_layout.addWidget(self.item_name)

        # 라디오버튼 생성
        radio_label = QLabel("추가할 데이터의 종류는 정상인가요, 불량인가요?")

        self.radio_good = QRadioButton("정상")
        self.radio_bad = QRadioButton("불량")
        radios = QHBoxLayout()
        radios.addWidget(self.radio_good)
        radios.addWidget(self.radio_bad)
        radio_layout = QVBoxLayout()
        radio_layout.addWidget(radio_label)
        radio_layout.addLayout(radios)
        
        # 파일 찾기 버튼 생성
        self.files = None
        file_label = QLabel("추가할 데이터 파일들을 선택해 주세요.")
        self.selected_files_label = QLabel()  # 선택된 파일 이름을 나타낼 라벨
        file_button = QPushButton("파일 찾기")
        file_button.clicked.connect(self.open_file_dialog)
        file_layout = QVBoxLayout()
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.selected_files_label)
        file_layout.addWidget(file_button)
        
        # Dialog layout 생성
        layout = QVBoxLayout()
        layout.addLayout(item_layout)
        layout.addSpacing(20)  # 간격 추가
        layout.addLayout(radio_layout)
        layout.addSpacing(20)  # 간격 추가
        layout.addLayout(file_layout)
        layout.addSpacing(20)  # 간격 추가
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.add_data)
        button_box.button(QDialogButtonBox.Ok).setText("확인")
        
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        dialog.exec_()

    def add_data(self):
        # 사용자가 입력한 데이터 이름 가져오기
        item_name_text = self.item_name.toPlainText().strip()
        
        if not item_name_text:
            QMessageBox.warning(self, "경고", "데이터 이름을 입력하세요.")
            return
        
        # 새 디렉터리 생성
        directory = os.path.join('data', item_name_text)
        os.makedirs(directory, exist_ok=True)
        
        # 정상 또는 불량에 따라 images/good 또는 images/bad 디렉터리 생성
        if self.radio_good.isChecked():
            directory = os.path.join(directory, "images", "good")
        elif self.radio_bad.isChecked():
            directory = os.path.join(directory, "images", "bad")
        else:
            QMessageBox.warning(self, "경고", "데이터 종류를 선택하세요.")
            return
        
        os.makedirs(directory, exist_ok=True)
        
        if not self.files:
            QMessageBox.warning(self, "경고", "추가할 데이터를 선택하세요.")
            return
        else:
            # 선택된 파일들을 복사해서 해당 디렉터리로 이동
            for file in self.files:
                shutil.copy(file, directory)
        
        QMessageBox.information(self, "완료", "데이터 추가가 완료되었습니다.")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        self.files, _ = QFileDialog.getOpenFileNames(self, "파일 선택", "", "All Files (*);;", options=options)
        if self.files:
            self.selected_files_label.setWordWrap(True)
            self.selected_files_label.setText("선택된 파일: " + ", ".join(self.files))

    def go_home(self):
        self.main_window.show()
        self.close()

    def closeEvent(self, event):
        # 닫힐 때 위치와 크기 정보 저장
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
#     window = DataWindow()
#     window.show()
#     sys.exit(app.exec_())
