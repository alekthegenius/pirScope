import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt
from picamera2.previews.qt import QPicamera2
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from picamera2.outputs import FfmpegOutput
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

video_config = picam2.create_video_configuration()
cfg = picam2.create_still_configuration(buffer_count=4, raw={'size': (1536, 864)})
preview_config = picam2.create_preview_configuration(main={"size": (480, 480)})

encoder = H264Encoder(bitrate=10000000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("pir Scope")
        self.setGeometry(0, 0, 480, 480)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create QPicamera2 widget
        
        self.qpicamera2 = QPicamera2(picam2, width=455, height=455, keep_ar=False)
        layout.addWidget(self.qpicamera2)

        # Create exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(25)
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.showFullScreen()

    def closeEvent(self, event):
        with picam2_lock:
            picam2.stop()
        event.accept()

def preview():
    with picam2_lock:
        picam2.configure(preview_config)

    app = QApplication([])

    
    main_window = MainWindow()
    
    with picam2_lock:
        picam2.start()

    main_window.show()
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
    prevRes = request.args.get('prevRes')
    afMode = request.args.get('afMode')
    camMode = request.args.get('cameraMode')

    if command is not None:
        date = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        if command == "TakePhoto":
            # Take photo
            file_path = photos_dir + f"img_{date}.jpg"
            print(f"File path: {file_path}")
            with picam2_lock:
            
                picam2.switch_mode_and_capture_file(cfg, file_path)
            
            return "Success"
        
        elif command == "prevRes":
            with picam2_lock:

                picam2.stop()

                #Update Preview Resolution
                width, height = map(int, prevRes.split('x'))
                new_preview_config = picam2.create_preview_configuration(main={"size": (width, height)})

                picam2.configure(new_preview_config)
                picam2.start()

            return "Success"

        elif command == "afMode":
            with picam2_lock:
                #Update AF Mode
                picam2.set_controls({"AfMode": afMode})
            return "Success"

        elif command == "camMode":
            with picam2_lock:

                picam2.stop()

                #Update Preview Resolution
                width, height = map(int, prevRes.split('x'))
                new_cfg_config = picam2.create_still_configuration(main={"size": (width, height)})

                picam2.configure(new_cfg_config)
                picam2.start()

            return "Success"


        elif command == "Restart":
            with picam2_lock:
                if picam2.recording:
                    picam2.stop_recording()
            

            call("sudo reboot", shell=True)


        elif command == "Shutdown":
            with picam2_lock:
                if picam2.recording:
                    picam2.stop_recording()

            call("sudo shutdown -h now", shell=True)


        return "Success"

    else:
        return "Invalid command", 400


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
