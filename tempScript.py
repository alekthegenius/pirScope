from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
from picamera2.previews.qt import QPicamera2
from picamera2 import Picamera2
import datetime

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

def on_button_clicked():
    button.setEnabled(False)
    cfg = picam2.create_still_configuration()
    picam2.switch_mode_and_capture_file(cfg, '/home/pi/Pictures/image{}.jpg'.format(datetime.datetime.now()), signal_function=qpicamera2.signal_done)

def capture_done(job):
    result = picam2.wait(job)
    button.setEnabled(True)

app = QApplication([])
qpicamera2 = QPicamera2(picam2, width=480, height=360, keep_ar=False)
button = QPushButton("Click to capture JPEG")
window = QWidget()
qpicamera2.done_signal.connect(capture_done)
button.clicked.connect(on_button_clicked)

layout_v = QVBoxLayout()
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button)
window.setWindowTitle("Qt Picamera2 App")
window.resize(480, 400)
window.setLayout(layout_v)

picam2.start()
window.show()
app.exec()