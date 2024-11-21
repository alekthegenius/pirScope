from picamera2.previews.qt import QPicamera2
from picamera2 import Picamera2
import datetime

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (480, 480)}))

app = QApplication([])
qpicamera2 = QPicamera2(picam2, width=480, height=480, keep_ar=False)

qpicamera2.setWindowTitle("Qt Picamera2 App")
qpicamera2.resize(480, 480)
qpicamera2.showFullScreen()

picam2.start()
app.exec()