from flask import Flask, Response, render_template
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
app = Flask(__name__)
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='face_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE)

landmarker =  FaceLandmarker.create_from_options(options) 
cap = cv2.VideoCapture(0)

def generate_frames():
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = landmarker.detect(mp_image)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            h, w, _ = frame.shape
            xs = [int(lm.x * w) for lm in landmarks]
            ys = [int(lm.y * h) for lm in landmarks]

            # Draw the landmark dots
            for x, y in zip(xs, ys):
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            # Define bounding box
            x1 = max(min(xs) - 20, 0)
            y1 = max(min(ys) - 20, 0)
            x2 = min(max(xs) + 20, w)
            y2 = min(max(ys) + 20, h)

            # Draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)