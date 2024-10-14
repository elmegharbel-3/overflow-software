import flask
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
app = flask.Flask(__name__)
# get the joystick data
latest_data = None
def make_get_request():
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
def get_data(): 
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Joy-Cam")
    window.setGeometry(100, 100, 800, 600)
    label = QLabel(window)
    start_button = QPushButton("Start Camera", window)
    stop_button = QPushButton("Stop Camera", window)
    joy_info = QLabel(window)
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(start_button)
    layout.addWidget(stop_button)
    layout.addWidget(joy_info)
    window.setLayout(layout)
    def start_camera(cap, timer):
        if cap[0] is None:
            cap[0] = cv2.VideoCapture(0)
            timer.start(20)
    def update_frame(cap, label):
        ret, frame = cap[0].read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(qt_image))
    def stop_camera(cap, timer, label):
        if cap[0] is not None:
            timer.stop()
            cap[0].release()
            cap[0] = None
            label.clear()
    def update_joy(data):
        joy_info.setText(data)
    cap = [None]
    timer = QTimer()
    timer.timeout.connect(lambda: update_frame(cap, label))
    start_button.clicked.connect(lambda: start_camera(cap, timer))
    stop_button.clicked.connect(lambda: stop_camera(cap, timer, label))
    timer_2 = QTimer()
    timer_2.timeout.connect(lambda: update_joy(latest_data))
    timer_2.start(100)    
    window.show()
    app.exec()
    global state
    state = True
    return latest_data     
if __name__ == '__main__':
    # run the get function in the background
    thread_1 = threading.Thread(target=make_get_request)
    thread_1.daemon = True
    thread_1.start()
    app.run(debug=True, port=8080,host="0.0.0.0",threaded=False)

    
