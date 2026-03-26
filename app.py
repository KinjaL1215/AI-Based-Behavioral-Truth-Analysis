from flask import Flask, Response, render_template
from face_test import generate_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    
    app.run(debug=True, use_reloader=False, threaded=True)
