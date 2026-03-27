import numpy as np
import sounddevice as sd
import librosa
# your mic

import sounddevice as sd

def record_audio(duration=3, fs=48000):  # ✅ SAFE SAMPLE RATE
    try:
        print(f"🎤 Recording for {duration} seconds...")

        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype='float32',
            device=9  # ✅ ONLY mic
        )

        sd.wait()
        print("✅ Recording finished.")

        return recording.flatten(), fs

    except Exception as ex:
        print("❌ Microphone Error:", ex)
        return None, None
def analyze_voice(audio, fs):
    if audio is None:
        raise ValueError("No audio")

    try:
        pitch_values = librosa.yin(audio, fmin=50, fmax=300)
        pitch = np.mean(pitch_values)
    except:
        pitch = 0

    energy = np.mean(audio**2)

    try:
        tempo, _ = librosa.beat.beat_track(y=audio, sr=fs)
        if isinstance(tempo, np.ndarray):
            tempo = float(np.mean(tempo))
        else:
            tempo = float(tempo)
    except Exception:
        tempo = 0.0

    return pitch, energy, tempo
def calculate_score(pitch, energy, tempo):
    """
    Calculates a stress/deception score based on pitch, energy, and tempo.

    Parameters:
    pitch (float): Average pitch in Hz
    energy (float): Average energy level
    tempo (float): Speech tempo in BPM

    Returns:
    int: Score (0-3)
    """
    score = 0
    if pitch > 130:  # High pitch indicates stress
        score += 1
    if energy < 0.0001 or energy > 0.05:  # Hesitation/pauses (low energy) or shouting (high energy)
        score += 1
    if tempo < 80:  # Slow speaking or stopping indicates telling a lie
        score += 1
    return score

def classify_result(score):
    """
    Classifies the result based on the score.

    Parameters:
    score (int): Calculated score

    Returns:
    str: "LIKELY TRUTH" or "POSSIBLE LIE"
    """
    if score >= 1:
        return "POSSIBLE LIE"
    else:
        return "LIKELY TRUTH"

if __name__ == "__main__":
    # Record audio
    audio, fs = record_audio(duration=5)

    # Analyze audio
    pitch, energy, tempo = analyze_voice(audio, fs)

    # Calculate score
    score = calculate_score(pitch, energy, tempo)

    # Classify result
    result = classify_result(score)

    # Print results
    print(f"Average Pitch: {pitch:.2f} Hz")
    print(f"Average Energy: {energy:.4f}")
    print(f"Speech Tempo: {tempo:.2f} BPM")
    print(f"Score: {score}")
    print(f"Result: {result}")
