import numpy as np
from flask import Flask, Response, render_template, jsonify
from face_test import generate_frames, shared_data
from voice import record_audio, analyze_voice, calculate_score, classify_result

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/blink_count')
def blink_count():
    return jsonify(count=shared_data["blink_count"])

@app.route('/voice_analysis')
def voice_analysis():
    try:
        audio, fs = record_audio()

        if audio is None:
            return jsonify({'error': 'Microphone not working'}), 500

        pitch, energy, tempo = analyze_voice(audio, fs)
        score = calculate_score(pitch, energy, tempo)
        result = classify_result(score)

        # Ensure tempo is scalar for JSON rounding
        if isinstance(tempo, (np.ndarray, list, tuple)):
            tempo = float(np.mean(tempo))
        else:
            tempo = float(tempo)

        return jsonify({
            'pitch': float(round(pitch, 2)),
            'energy': float(round(energy, 4)),
            'tempo': float(round(tempo, 2)),
            'score': float(score),
            'result': str(result),
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    
    app.run(debug=True, use_reloader=False, threaded=True)
