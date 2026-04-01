import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from models.blink import BlinkDetector
from models.facial_expression import predict_tension_from_facial_expression
import os

# ✅ Shared Data
shared_data = {
    "blink_count": 0,
    "facial_prediction": "Calibrating",
    "lie_probability": 0
}

# ✅ Globals (DO NOT LOAD HERE)
detector = None
blink_detector = BlinkDetector()


# ✅ Lazy Loader for MediaPipe (CRITICAL FIX)
def get_detector():
    global detector

    if detector is None:
        model_path = os.path.join(
            os.path.dirname(__file__),
            "face_landmarker.task"
        )

        # 🔥 Safety check
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        base_options = python.BaseOptions(
            model_asset_path=model_path,
            delegate=python.BaseOptions.Delegate.CPU
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            output_face_blendshapes=True
        )

        detector = vision.FaceLandmarker.create_from_options(options)

    return detector

# ✅ Main Processing Function
def analyze_frame(frame, session_history=None):
    global shared_data

    detector = get_detector()   # 🔥 Lazy load here

    # 1. Convert OpenCV → MediaPipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    # 2. Detect
    result = detector.detect(mp_image)

    if result.face_landmarks:
        landmarks_raw = result.face_landmarks[0]
        landmark_points = [(lm.x, lm.y) for lm in landmarks_raw]

        # 3. Blink
        shared_data["blink_count"] = blink_detector.detect_blink(landmarks_raw)

        # 4. Tension
        prediction, _ = predict_tension_from_facial_expression(
            landmark_points,
            baseline_dist=0.05
        )
        shared_data["facial_prediction"] = prediction

        # 5. Session tracking
        if session_history and session_history.get("is_active"):
            session_history["total_frames"] += 1
            if "Tense" in prediction:
                session_history["tension_count"] += 1
    else:
        shared_data["facial_prediction"] = "No Face Detected"
    return shared_data