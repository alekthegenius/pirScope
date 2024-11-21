#!/usr/bin/python3

import time
from flask import Flask, render_template, request

from picamera2 import Picamera2, Preview

stop = False

app = Flask(__name__)

picam2 = Picamera2()
picam2.start_preview(Preview.QT)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)


@app.route('/', methods=['GET'])
def control():
    command = request.args.get('command')
    if command is not None:
        
        if command == "photo":
            picam2.capture_file("photo.jpg")

        return render_template("command.html")

    else:
        return render_template("index.html")


if __name__ == "__main__":
    picam2.start()

    while not stop:
        app.run(host="0.0.0.0", port=8080, debug=True)
