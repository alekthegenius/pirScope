from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start_preview(Preview.QT)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)

picam2.start()
