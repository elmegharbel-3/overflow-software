import cv2
import threading
import time
from flask import Flask, Response, render_template

app = Flask(__name__)

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

""" @app.route('/camera2')
def video_feed2():
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame') """
""" @app.route('/')
def home():
    return render_template("cam.html") """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)