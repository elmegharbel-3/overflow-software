import cv2
from flask import Flask, render_template, Response, jsonify, request
import requests
import threading
from flask_cors import CORS
import json
import multiprocessing as mp

app = Flask(__name__)
CORS(app)
# Initialize a list of camera indices
camera_indices = [0,1]  # Assuming you have two cameras
filename = "C:\main\Programming\overflow\OVERFLOW\gui\json\camera_data.json"
camera_streams = {}
with open(filename,"r") as file:
    cam_data = json.load(file)
JOYSTICK_SERVER_URL = 'http://192.168.137.1:5000/joystick'  # Change this to your joystick server's IP and port
def get_camera_stream(camera_index):
    """Capture camera feed from a specific index and handle errors."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[INFO] Camera {camera_index} is not available.")
        return None

    def generate():
        frame_counter = 0
        while True:
            success, frame = cap.read()
            if not success:
                print(f"[ERROR] Failed to read frame from camera {camera_index}.")
                break
            frame_counter += 1
            if frame_counter % 3 == 0:  # Process every 3rd frame
                continue
            # Resize frame to reduce resolution and improve performance
            frame = cv2.resize(frame, (320, 240))
            # Convert frame to JPEG with reduced quality
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), int(cam_data[str(camera_index)])])
            frame = buffer.tobytes()

            # Yield frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return generate

@app.route('/')
def index():
    # Pass the list of available camera indices to the template
    return render_template('index.html', available_cameras=camera_indices)

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    """Video streaming route. Put this in the src attribute of an img tag."""
    stream = camera_streams.get(camera_index)
    if stream:
        return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        # Handle case when a camera feed is unavailable
        return "Camera feed is not available", 404
@app.route('/video_feed/<int:camera_index>/quality',methods=["POST","GET"])
def quality(camera_index):
    if request.method == "POST":
        print(request.json)
        theIndex = request.json.get("index")
        print(request.json.get("index"))
        theQuality = request.json.get("quality")
        print(request.json.get("quality"))
        with open(filename,"r") as file:
            global cam_data
            cam_data = json.load(file)
        cam_data[theIndex] = int(theQuality)
        with open(filename,"w") as file:
            json.dump(cam_data,file)
        return "hello from inside"
    else: return "hello from outside"
        


@app.route('/remote_joystick', methods=['GET'])
def get_remote_joystick_status():
    try:
        response = requests.get(JOYSTICK_SERVER_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def initialize_camera_streams():
    """Initialize camera streams in separate threads."""
    for index in camera_indices:
        stream = get_camera_stream(index)
        if stream:
            camera_streams[index] = stream
            print(stream)
            """ threading.Thread(target=stream, daemon=True).start() """
            func = mp.Process(target=stream)
        else:
            print(f"[INFO] Camera {index} is not available and won't be started.")

if __name__ == '__main__':
    initialize_camera_streams()
    app.run(host='0.0.0.0', port=5000, debug=True)
