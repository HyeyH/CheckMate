from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTreeView, QFileSystemModel, QMessageBox, QFileDialog, QDialogButtonBox
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
        home_button.clicked.connect(self.close)  # 윈도우를 닫는 버튼
        home_button.setStyleSheet("border: none;")
        home_button.setToolTip("홈으로")

        # 제목 레이블 생성
        self.title_label = QLabel('데이터')
        self.title_font = QFont(self.font_family, 20, QFont.Bold)
        self.title_label.setFont(self.title_font)

        # 부제목 레이블 생성
        self.subtitle_label = QLabel('체크메이트 사용을 위한 데이터셋 관리를 위한 창입니다.\n해당 창에서 추가한 데이터셋과 라벨링한 데이터셋을 통해 체크메이트를 학습 시킬 수 있습니다.')
        self.subtitle_font = QFont(self.font_family, 10, QFont.Normal)
        self.subtitle_label.setFont(self.subtitle_font)

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

        # 데이터 추가 버튼 생성
        self.add_button = QPushButton('데이터셋 추가')
        self.add_button.clicked.connect(self.add_data)
        self.add_button.setToolTip("물품에 대한 새로운 이미지를 추가합니다.")

        # 데이터 수정 버튼 생성
        self.label_button = QPushButton('데이터셋 라벨링')
        self.label_button.clicked.connect(self.label_data)
        self.label_button.setToolTip("추가한 데이터에 대한 라벨링을 진행합니다.")

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.addWidget(home_button, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.subtitle_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.label_button)

        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.button_layout)
        hbox_layout.addLayout(main_layout)
        self.setLayout(hbox_layout)

    def save_yaml_file(self, file_path, data):
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

    def load_yaml_file(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    def label_data(self):
        parent_directory = os.path.dirname('..')
        # 현재는 exe 파일로 해 두었지만, 추후 해당 소스 수정
        exe_path = os.path.join(parent_directory, 'labelImg.exe')
        if os.path.exists(exe_path) and os.access(exe_path, os.X_OK):
            subprocess.Popen([exe_path])

            # 사용자가 원하는 디렉토리 선택 다이얼로그 표시
            selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory", parent_directory)
            if selected_directory:
                try:
                    # train, val 디렉토리 설정 및 names 값 읽기
                    train_directory = os.path.join(selected_directory, 'images')
                    val_directory = os.path.join(selected_directory, 'images')
                    labels_directory = os.path.join(selected_directory, 'labels')  # labels 디렉토리 경로

                    # labels 디렉토리가 없는 경우 생성
                    os.makedirs(labels_directory, exist_ok=True)

                    names_path = os.path.join(labels_directory, 'classes.txt')

                    # names 값 읽어오기
                    with open(names_path, 'r') as file:
                        names = {}
                        for line in file:
                            index, name = line.strip().split(':', 1)
                            names[int(index)] = name.strip()

                    # data 설정
                    data = {'train': train_directory, 'val': val_directory, 'names': names, 'nc': 2}
                    yaml_file_path = os.path.join(selected_directory, 'data.yaml')
                    self.save_yaml_file(yaml_file_path, data)
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "데이터 라벨링을 진행할 수 없습니다.")

    def add_data(self):
        # 사용자에게 정상인지 불량인지 묻는 다이얼로그
        reply = QMessageBox.question(self, 'Confirmation', '추가할 데이터는 정상 제품인가요?', QMessageBox.Yes | QMessageBox.No)

        # 사용자가 선택한 폴더
        selected_folder_path = None
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        # 상위 디렉토리의 data 폴더로 초기 경로 설정
        current_path = os.path.dirname(os.path.abspath(__file__))
        data_directory = os.path.join(os.path.dirname(current_path), 'data')
        folder_dialog.setDirectory(data_directory)

        # 정상인 경우 선택한 폴더에 "good" 디렉터리 생성
        if reply == QMessageBox.Yes:
            if folder_dialog.exec_():
                selected_folder_path = folder_dialog.selectedFiles()[0]
                good_folder_path = os.path.join(selected_folder_path, 'images/good')
                os.makedirs(good_folder_path, exist_ok=True)

        # 불량인 경우 선택한 폴더에 "bad" 디렉터리 생성
        else:
            if folder_dialog.exec_():
                selected_folder_path = folder_dialog.selectedFiles()[0]
                bad_folder_path = os.path.join(selected_folder_path, 'images/bad')
                os.makedirs(bad_folder_path, exist_ok=True)

        # 선택한 폴더가 있는 경우 파일을 해당 폴더로 복사
        if selected_folder_path:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFiles)
            file_dialog.setViewMode(QFileDialog.List)

            # 상위 디렉토리의 data 폴더로 초기 경로 설정
            file_dialog.setDirectory(data_directory)

            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    for selected_file_path in selected_files:
                        file_name = os.path.basename(selected_file_path)
                        if reply == QMessageBox.Yes:
                            destination_file_path = os.path.join(good_folder_path, file_name)
                        else:
                            destination_file_path = os.path.join(bad_folder_path, file_name)
                        shutil.copy(selected_file_path, destination_file_path)
                    QMessageBox.information(self, "Add Data", f"성공적으로 데이터가 추가되었습니다.: {selected_folder_path}")

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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = DataWindow()
#     window.show()
#     sys.exit(app.exec_())
