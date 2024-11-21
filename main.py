#!/usr/bin/python3

import time
import datetime
from flask import Flask, render_template, request
from picamera2 import Picamera2, Preview
from subprocess import call

stop = False

app = Flask(__name__)

imageDate = ""

picam2 = Picamera2()
picam2.start_preview(Preview.QT)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)


@app.route('/', methods=['GET'])
def control():
    command = request.args.get('command')
    if command is not None:
        imageDate = str(datetime.datetime.now())
        
        if command == "Photo":
            picam2.capture('/home/pi/Pictures/image{}.jpg'.format(imageDate))

        elif command == "StartRecording":
            picam2.start_recording('/home/pi/Videos/video{}.h264'.format(imageDate))

        elif command == "StopRecording":
            picam2.stop_recording()

        elif command == "Restart":
            picam2.stop_preview()
            picam2.stop_recording()
            picam2.close()


        elif command == "Shutdown":
            call("sudo shutdown -h now", shell=True)

        return render_template("command.html")

    else:
        return render_template("index.html")


if __name__ == "__main__":
    picam2.start()

    while not stop:
        app.run(host="0.0.0.0", port=8080, debug=True)
