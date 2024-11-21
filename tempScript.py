from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
from picamera2.previews.qt import QPicamera2
from picamera2 import Picamera2
import datetime

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

app = QApplication([])
qpicamera2 = QPicamera2(picam2, width=480, height=400, keep_ar=False)

qpicamera2.setWindowTitle("Qt Picamera2 App")
qpicamera2.resize(480, 400)

picam2.start()
qpicamera2.show()
app.exec()