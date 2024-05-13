import random
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTreeView, QFileSystemModel, QMessageBox, QFileDialog, QDialogButtonBox, QLineEdit, QRadioButton, QComboBox, QTextEdit
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QDir
import sys, os
import subprocess
import shutil
import yaml
from labelImg_tutorial import TutorialDialog


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
        dialog = QDialog()
        dialog.resize(500, 400)
        layout = QVBoxLayout()

        self.directory_combo = QComboBox()
        self.populate_directory_combo()
        layout.addWidget(self.directory_combo)
        
        # 비율을 지정하기 위한 레이블과 입력 필드를 추가합니다.
        self.ratio_label = QLabel("데이터 분할 비율을 선택해 주세요. 순서대로 train:valid:test 입니다.")
        layout.addWidget(self.ratio_label)

        self.radio_602020 = QRadioButton("60:20:20")
        self.radio_603010 = QRadioButton("60:30:10")
        self.radio_702010 = QRadioButton("70:20:10")
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_602020)
        radio_layout.addWidget(self.radio_603010)
        radio_layout.addWidget(self.radio_702010)    
        layout.addLayout(radio_layout)

        # 분할 버튼을 추가합니다.
        self.split_button = QPushButton("데이터 분할")
        self.split_button.clicked.connect(self.split_data)
        layout.addWidget(self.split_button)

        dialog.setLayout(layout) 
        dialog.exec_()

    def populate_directory_combo(self):
        # './data' 디렉터리에서 디렉터리 명들을 읽어와 콤보박스에 추가합니다.
        directory = './data'
        directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        self.directory_combo.addItems(directories)

    def split_data(self):
        directory_name = self.directory_combo.currentText()

        if not directory_name:
            QMessageBox.warning(self, "경고", "폴더를 선택하세요.")
            return

        if self.radio_603010.isChecked():
            ratio_text = "60:30:10"
        elif self.radio_602020.isChecked():
            ratio_text = "60:20:20"
        elif self.radio_702010.isChecked():
            ratio_text = "70:20:10"
        else:
            QMessageBox.warning(self, "경고", "원하는 분할 비율을 선택하세요.")
            return

        # Check if labels directory is empty
        labels_dir = os.path.join('./data', directory_name, 'labels')
        if not os.listdir(labels_dir):
            QMessageBox.warning(self, "경고", "선택한 폴더의 labels 디렉터리가 비어 있습니다.")
            return

        try:
            # 입력된 비율을 ':'로 분할하여 train, valid, test 비율로 나눕니다.
            ratios = ratio_text.split(':')
            if len(ratios) != 3:
                QMessageBox.warning(self, "Error", "올바른 비율을 입력하세요.")
                return
            train_ratio, valid_ratio, test_ratio = map(float, ratios)
            total_ratio = train_ratio + valid_ratio + test_ratio

            # 디렉터리 생성
            train_dir = os.path.join('./data', directory_name, 'train')
            valid_dir = os.path.join('./data', directory_name, 'valid')
            test_dir = os.path.join('./data', directory_name, 'test')

            # 이미지 및 레이블 폴더 생성
            for directory in [train_dir, valid_dir, test_dir]:
                os.makedirs(os.path.join(directory, 'images'), exist_ok=True)
                os.makedirs(os.path.join(directory, 'labels'), exist_ok=True)

            # 이미지 및 레이블 파일 목록 가져오기
            source_dir_good_images = os.path.join('./data', directory_name, 'good')
            source_dir_labels = os.path.join('./data', directory_name, 'labels')
            source_dir_bad_images = os.path.join('./data', directory_name, 'bad')

            filenames_good = os.listdir(source_dir_good_images)
            filenames_bad = os.listdir(source_dir_bad_images)

            # 분할된 파일 수 계산
            # 수정 필요해 보임... ㅜㅜ
            total_good_files = len(filenames_good)
            total_bad_files = len(filenames_bad)

            train_count_good = int(train_ratio / total_ratio * total_good_files)
            valid_count_good = int(valid_ratio / total_ratio * total_good_files)
            test_count_good = total_good_files - train_count_good - valid_count_good

            train_count_bad = int(train_ratio / total_ratio * total_bad_files)
            valid_count_bad = int(valid_ratio / total_ratio * total_bad_files)
            test_count_bad = total_bad_files - train_count_bad - valid_count_bad

            # 최종 분할된 파일 수는 good과 bad 중 더 작은 수를 선택하여 설정
            train_count = train_count_good + train_count_bad
            valid_count = valid_count_good + valid_count_bad
            test_count = test_count_good + test_count_bad

            # 이미지 및 레이블 파일 분할
            for directory, count in zip([train_dir, valid_dir, test_dir], [train_count, valid_count, test_count]):
                for filename in filenames_good[:count]:
                    # good 이미지와 레이블 파일 복사
                    shutil.copy(os.path.join(source_dir_good_images, filename), os.path.join(directory, 'images', filename))
                    shutil.copy(os.path.join(source_dir_labels, filename.replace('.jpg', '.txt')), os.path.join(directory, 'labels', filename.replace('.jpg', '.txt')))
                
                for filename in filenames_bad[:count]:
                    # bad 이미지와 레이블 파일 복사
                    shutil.copy(os.path.join(source_dir_bad_images, filename), os.path.join(directory, 'images', filename))
                    shutil.copy(os.path.join(source_dir_labels, filename.replace('.jpg', '.txt')), os.path.join(directory, 'labels', filename.replace('.jpg', '.txt')))
                
                filenames_good = filenames_good[count:]
                filenames_bad = filenames_bad[count:]

            QMessageBox.information(self, "완료", "데이터 분할이 완료되었습니다.")
        except Exception as e:
            print("에러:", e)
        
    
    def open_label_data(self):
        dialog = QDialog()
        dialog.resize(500, 400)
        layout = QVBoxLayout()
        label = QLabel("데이터를 라벨링할 물품의 이름을 하나만 입력하세요. 예) eraser")
        layout.addWidget(label)
        text_edit = QTextEdit()
        text_edit.setFixedHeight(30)
        layout.addWidget(text_edit)
        button_ok = QPushButton("확인")

        def on_button_ok_clicked():
            item_name = text_edit.toPlainText().strip()  # text_edit의 텍스트를 가져옴 (양쪽 공백 제거)
            if not item_name:
                QMessageBox.warning(self, "경고", "물품명을 입력하세요.")
                return
            else:
                image_directory = os.path.join("data", item_name)
                good_directory = os.path.join(image_directory, "good")
                bad_directory = os.path.join(image_directory, "bad")
                # good 디렉터리가 존재하고 비어 있지 않은지 확인
                if os.path.exists(good_directory):
                    if not os.listdir(good_directory):
                        QMessageBox.warning(self, "경고", "Good 디렉터리에 이미지가 있어야 합니다.")
                        return
                # bad 디렉터리가 존재하고 비어 있지 않은지 확인
                elif os.path.exists(bad_directory):
                    if not os.listdir(bad_directory):
                        QMessageBox.warning(self, "경고", "Bad 디렉터리에 이미지가 있어야 합니다.")
                        return
                else:
                    QMessageBox.information(self, "라벨링 가능", "해당 물품은 라벨링이 가능합니다.")
                    os.makedirs(os.path.join(image_directory, "labels"), exist_ok=True)
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
            tutorial_dialog = TutorialDialog()
            tutorial_dialog.exec_()
            process.wait()
        else:
            QMessageBox.warning(self, "Error", "데이터 라벨링을 진행할 수 없습니다.")

    def open_add_data(self):
        dialog = QDialog(self)
        dialog.setFont(QFont(self.font_family))
        dialog.setWindowTitle("데이터 추가")
        dialog.resize(500, 400)
        item_label = QLabel("추가할 데이터의 이름을 영문으로 작성해 주세요. 예) eraser, milk")

        self.item_name = QTextEdit()  
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
        
        # 정상 또는 불량에 따라 good 또는 bad 디렉터리 생성
        if self.radio_good.isChecked():
            directory = os.path.join(directory, "good")
        elif self.radio_bad.isChecked():
            directory = os.path.join(directory, "bad")
        else:
            QMessageBox.warning(self, "경고", "데이터 종류를 선택하세요.")
            return
        
        os.makedirs(directory, exist_ok=True)
        
        if not self.files:
            QMessageBox.warning(self, "경고", "추가할 데이터를 선택하세요.")
            return
        else:
            # 선택된 파일들을 복사해서 해당 디렉터리로 이동
            for i, file in enumerate(self.files):
                # 파일명과 확장자를 분리
                filename, extension = os.path.splitext(file)
                # 새로운 파일명 생성
                new_filename = 'g{}'.format(i) if self.radio_good.isChecked() else 'b{}'.format(i)
                new_filepath = os.path.join(directory, new_filename + extension)
                shutil.copy(file, new_filepath)
        
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
