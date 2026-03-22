from flask import Flask, Response
import cv2

app = Flask(__name__)

camera = None


def set_camera(cap):
    global camera
    camera = cap


def generate_frames():
    while True:
        if camera is None:
            continue
        ret, frame = camera.read()
        if not ret:
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
        )


@app.route('/')
def stream():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


def start_stream():
    app.run(host='0.0.0.0', port=5000, threaded=True)
