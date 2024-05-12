from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class TutorialDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.currentPage = 1
        self.initUI()

    def initUI(self):
        self.setWindowTitle("설명서")
        self.layout = QVBoxLayout()
        self.resize(400, 500)
        self.labels = [
            "Open Dir로 라벨링을 원하는 물품 폴더의 good 또는 bad 폴더를 선택하세요.",
            "Change Save Dir로 라벨링을 원하는 물품 폴더의 labels 폴더를 선택해 주세요.",
            "PascalVOC를 눌러 YOLO로 바꾼다... 이거 맞음??"
            "Create Rect Box로 이미지를 지정해 class를 선택한 후 save 버튼 혹은 Ctrl+S를 눌러 사각형을 저장합니다.",
            "데이터 관리 화면으로 돌아와 해당 물품의 labels 폴더에 저장이 되었는지 확인합니다."
        ]
        self.label = QLabel(self.labels[self.currentPage - 1])
        self.layout.addWidget(self.label)

        # 페이지 수를 표시하는 레이아웃 추가
        self.page_layout = QHBoxLayout()
        self.page_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.page_layout)

        self.prev_button = QPushButton("이전")
        self.prev_button.clicked.connect(self.prevPage)
        self.page_layout.addWidget(self.prev_button)

        self.page_label = QLabel(f"페이지: {self.currentPage}/{len(self.labels)}")
        self.page_layout.addWidget(self.page_label)

        self.next_button = QPushButton("다음")
        self.next_button.clicked.connect(self.nextPage)
        self.page_layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        # 다이얼로그를 오른쪽에 위치시킵니다.
        screen_geometry = QApplication.desktop().screenGeometry()
        dialog_geometry = self.geometry()
        self.move(screen_geometry.width() - dialog_geometry.width(), int((screen_geometry.height() - dialog_geometry.height()) / 2))

    def nextPage(self):
        self.currentPage += 1
        if self.currentPage <= len(self.labels):
            self.label.setText(self.labels[self.currentPage - 1])
            self.page_label.setText(f"페이지: {self.currentPage}/{len(self.labels)}")
        else:
            self.currentPage = len(self.labels)
    
    def prevPage(self):
        self.currentPage -= 1
        if self.currentPage >= 1:
            self.label.setText(self.labels[self.currentPage - 1])
            self.page_label.setText(f"페이지: {self.currentPage}/{len(self.labels)}")
        else:
            self.currentPage = 1

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = TutorialDialog()
    dialog.exec_()
