from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QListView, QFileSystemModel, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QModelIndex
import sys


class DataWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CheckMate - Data Management')
        self.resize(800, 600)

        # 윈도우를 화면 가운데에 위치시키기
        self.center_window()

        # 버튼 생성
        home_button = QPushButton(self)
        home_button.setIcon(QIcon("home.png"))  # 그림 파일 경로를 지정하여 아이콘 설정
        home_button.clicked.connect(self.close)  # 윈도우를 닫는 버튼
        home_button.setStyleSheet("border: none;")

        # 제목 레이블 생성
        self.title_label = QLabel('DATA')
        self.title_font = QFont("Arial", 20, QFont.Bold)
        self.title_label.setFont(self.title_font)

        # 데이터 폴더 표시를 위한 QListView 및 모델 생성
        self.list_view = QListView()
        self.data_model = QFileSystemModel()
        self.data_model.setRootPath('./data')
        self.list_view.setModel(self.data_model)
        self.list_view.setRootIndex(self.data_model.index('.'))


        # 데이터 수정 버튼 생성
        self.add_button = QPushButton('Add Data')
        self.add_button.clicked.connect(self.add_data)
        # 데이터 수정 버튼 생성
        self.modify_button = QPushButton('Modify Data')
        self.modify_button.clicked.connect(self.modify_data)

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.addWidget(home_button, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.list_view)
        main_layout.addWidget(self.modify_button)
        main_layout.addWidget(self.add_button)

        self.setLayout(main_layout)

    def modify_data(self):
        # 선택된 항목 수정
        index = self.list_view.currentIndex()
        item_path = self.data_model.filePath(index)
        QMessageBox.information(self, "Modify Data", f"Modifying data: {item_path}")
    def add_data(self):
        # 선택된 항목 수정
        index = self.list_view.currentIndex()
        item_path = self.data_model.filePath(index)
        QMessageBox.information(self, "Add Data", f"Adding data: {item_path}")
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
    window = DataWindow()
    window.show()
    sys.exit(app.exec_())
