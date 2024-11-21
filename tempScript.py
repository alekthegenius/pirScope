from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from picamera2.previews.qt import QPicamera2
from picamera2 import Picamera2
import datetime
import sys

class MainWindow(QMainWindow):
    def __init__(self, picam2):
        super().__init__()
        self.picam2 = picam2
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Qt Picamera2 App")
        self.setGeometry(0, 0, 480, 480)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create QPicamera2 widget
        self.qpicamera2 = QPicamera2(self.picam2, width=440, height=440, keep_ar=False)
        layout.addWidget(self.qpicamera2)

        # Create exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(40)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.showFullScreen()

    def closeEvent(self, event):
        self.picam2.stop()
        event.accept()

if __name__ == "__main__":
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (480, 480)}))

    app = QApplication(sys.argv)
    
    main_window = MainWindow(picam2)
    
    picam2.start()
    sys.exit(app.exec_())