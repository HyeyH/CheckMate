import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QTransform
from PyQt5.QtCore import Qt, QPoint, QRect

class ImageEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        self.load_button.move(20, 20)

        self.crop_button = QPushButton("Crop", self)
        self.crop_button.clicked.connect(self.crop_image)
        self.crop_button.setEnabled(False)
        self.crop_button.move(120, 20)

        self.rotate_button = QPushButton("Rotate", self)
        self.rotate_button.clicked.connect(self.rotate_image)
        self.rotate_button.setEnabled(False)
        self.rotate_button.move(220, 20)

        self.undo_button = QPushButton("Undo", self)
        self.undo_button.clicked.connect(self.undo_crop)
        self.undo_button.setEnabled(False)
        self.undo_button.move(320, 20)

        self.redo_button = QPushButton("Redo", self)
        self.redo_button.clicked.connect(self.redo_crop)
        self.redo_button.setEnabled(False)
        self.redo_button.move(420, 20)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        self.save_button.move(520, 20)

        self.image = None
        self.original_image = None
        self.start_point = None
        self.end_point = None
        self.counter_good = 0
        self.counter_bad = 0
        self.undo_stack = []
        self.redo_stack = []

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image files (*.jpg *.png *.bmp)")
        if filename:
            self.image = QImage(filename)
            self.original_image = self.image.copy()
            self.display_image()
            self.crop_button.setEnabled(True)
            self.rotate_button.setEnabled(True)
            self.redo_button.setEnabled(False)
            self.undo_button.setEnabled(False)
            self.undo_stack = []
            self.redo_stack = []

    def display_image(self):
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.image is not None:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.image is not None and event.buttons() == Qt.LeftButton:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.image is not None:
            self.end_point = event.pos()
            self.update()
            self.crop_button.setEnabled(True)

    def paintEvent(self, event):
        if self.start_point is not None and self.end_point is not None:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(rect)
            self.image_label.setPixmap(QPixmap.fromImage(self.image))

    def crop_image(self):
        if self.image is not None and self.start_point is not None and self.end_point is not None:
            rect = QRect(self.start_point, self.end_point).normalized()
            cropped_image = self.image.copy(rect)
            self.undo_stack.append(self.image.copy())
            self.image = cropped_image.copy()
            self.display_image()
            self.undo_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.redo_stack = []


    def undo_crop(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.display_image()
            if not self.undo_stack:
                self.undo_button.setEnabled(False)
                self.redo_button.setEnabled(True)

    def redo_crop(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.display_image()
            if not self.redo_stack:
                self.redo_button.setEnabled(False)
                self.undo_button.setEnabled(True)

    def rotate_image(self):
        if self.image is not None:
            self.image = self.image.transformed(QTransform().rotate(90))
            self.display_image()

    def save_image(self):
        if self.image is not None:
            reply = QMessageBox.question(self, 'Save Image', 'Is the image defective?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                directory = os.path.join('data', 'bad')
                filename = os.path.join(directory, f"{self.counter_bad}.png")
                self.counter_bad += 1
            else:
                directory = os.path.join('data', 'good')
                filename = os.path.join(directory, f"{self.counter_good}.png")
                self.counter_good += 1
                
            if not os.path.exists(directory):
                os.makedirs(directory)

            self.image.save(filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditorWindow()
    window.setGeometry(100, 100, 640, 480)
    window.show()
    sys.exit(app.exec_())
