import math

class BlinkDetector:
    def __init__(self, threshold=0.18): # Lowered default slightly for better accuracy
        self.threshold = threshold
        self.blink_count = 0
        self.blinking = False
    
    def eye_aspect_ratio(self, landmarks, eye_indices):
        # Indices: p1(inner), p2/p6(top/bottom), p3/p5(top/bottom), p4(outer)
        p1, p2, p3, p4, p5, p6 = [landmarks[i] for i in eye_indices]
        
        # Vertical distances
        v1 = math.dist((p2.x, p2.y), (p6.x, p6.y))
        v2 = math.dist((p3.x, p3.y), (p5.x, p5.y))
        # Horizontal distance
        h = math.dist((p1.x, p1.y), (p4.x, p4.y))
        
        return (v1 + v2) / (2.0 * h) if h != 0 else 1.0
    
    def get_current_ear(self, landmarks):
        # Standard MediaPipe indices for EAR
        left_eye = [33, 160, 158, 133, 153, 144]
        right_eye = [362, 385, 387, 263, 373, 380]
        
        l_ear = self.eye_aspect_ratio(landmarks, left_eye)
        r_ear = self.eye_aspect_ratio(landmarks, right_eye)
        return (l_ear + r_ear) / 2.0

    def detect_blink(self, landmarks):
        ear = self.get_current_ear(landmarks)
        
        # Logic: If EAR drops below threshold, it's a blink
        if ear < self.threshold:
            if not self.blinking:
                self.blink_count += 1
                self.blinking = True
        else:
            self.blinking = False
        
        return self.blink_count

    def set_threshold(self, natural_ear):
        # A blink is typically 60-70% of the natural open-eye EAR
        self.threshold = natural_ear * 0.65
        # print(f"Blink Threshold calibrated to: {self.threshold:.4f}")