from flask import Flask, request, Request, render_template,Response
import requests
import json
import time
import threading
import PyQt5
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
app = Flask(__name__)
# get the joystick data
latest_data = None
camera1 = cv2.VideoCapture(0)
def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera1')
def video_feed1():
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame') 
@app.route("/joystick", methods=["GET", "POST"])
def joystick_data():
    global latest_data
    while True:
        time.sleep(0.1)   
        try:
            response = requests.get("http://192.168.1.17:8080/joystick")
            if response.status_code == 200:
                latest_data = response.text
                print(latest_data)
            else:
                latest_data = {"error": f"Status Code: {response.status_code}"}
        except Exception as e:
            latest_data = json.dumps({"error": str(e)}), 500
@app.route('/', methods=["GET"])
def index(): 
    while True:
        return render_template("index.html")  
if __name__ == '__main__':
    # run the get function in the background
    thread_1 = threading.Thread(target=joystick_data)
    thread_1.daemon = True
    thread_1.start()
    app.run(debug=True, port=8080,host="0.0.0.0",threaded=False)