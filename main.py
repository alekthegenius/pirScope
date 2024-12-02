import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from picamera2.previews.qt import QPicamera2
from picamera2 import Picamera2
import datetime
import sys
from flask import Flask, render_template, request
from subprocess import call
from pathlib import Path
import os
import glob

picam2_lock = threading.Lock()

photos_dir = "./static/photos/"

if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)


picam2 = Picamera2()
imageDate = ""
app = Flask(__name__)

cfg = picam2.create_still_configuration(buffer_count=4, raw={'size': (1536, 864)})

class MainWindow(QMainWindow):
    def __init__(self, picam2):
        super().__init__()
        self.picam2 = picam2
        self.initUI()

    def initUI(self):
        self.setWindowTitle("pir Scope")
        self.setGeometry(0, 0, 480, 480)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create QPicamera2 widget
        self.qpicamera2 = QPicamera2(self.picam2, width=455, height=455, keep_ar=False)
        layout.addWidget(self.qpicamera2)

        # Create exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(25)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.showFullScreen()

    def closeEvent(self, event):
        self.picam2.stop()
        event.accept()

def preview():
    picam2.configure(picam2.create_preview_configuration(main={"size": (480, 480)}))

    app = QApplication(sys.argv)
    
    main_window = MainWindow(picam2)
    
    with picam2_lock:
        picam2.start()

    sys.exit(app.exec_())


@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/photos', methods=['GET'])
def photo():
    files = glob.glob(photos_dir + "*.jpg")
    filenames = [os.path.basename(x) for x in files]
    print(filenames)

    return render_template("photos.html", files=filenames)

@app.route('/control', methods=['POST'])
def control():
    command = request.args.get('command')
    if command is not None:
        imageDate = str(datetime.datetime.now())
        
        if command == "TakePhoto":
            # Take photo
            file_path = photos_dir + f"img_{imageDate}.jpg"
            print(f"File path: {file_path}")
            with picam2_lock:
                picam2.switch_mode_and_capture_file(cfg, file_path)

        elif command == "StartRecording":
            # Start Recording 
            pass

        elif command == "StopRecording":
            # Stop recording
            pass

        elif command == "Restart":
            call("sudo restart", shell=True)


        elif command == "Shutdown":
            call("sudo shutdown -h now", shell=True)

        return "Success"

    else:
        return "Error"


def frontend():
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)



# Create threads for each script
serveThread = threading.Thread(target=preview, daemon=True)
previewThread = threading.Thread(target=frontend, daemon=True)

# Start both threads
try:
    serveThread.start()
    previewThread.start()

    serveThread.join()
    previewThread.join()
except Exception as e:
    print(e)
