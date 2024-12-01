import datetime
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/control', methods=['POST'])
def control():
    command = request.args.get('command')
    if command is not None:
        imageDate = str(datetime.datetime.now())
        
        if command == "TakePhoto":
            # Take photo
            print(f"Taking photo titled: img_{imageDate}.jpg")

        elif command == "StartRecording":
            # Start Recording 
            print("Starting Video")

        elif command == "StopRecording":
            # Stop recording
            print("Stopping Video")

        elif command == "Restart":
            print("Restarting Pi")


        elif command == "Shutdown":
            print("Shutting down Pi")

        return "Success"

    else:
        return "Error"


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080, debug=True)
    except Exception as e:
        print(e)
