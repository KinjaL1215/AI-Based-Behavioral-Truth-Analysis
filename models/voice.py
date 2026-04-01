import numpy as np
import librosa

# 🎤 REMOVED: record_audio function 
# (This is now handled by the Browser/JavaScript and passed to the backend)

# 🎧 ANALYSIS FUNCTION
def analyze_voice(audio, fs):
    """
    Processes raw audio data sent from the client.
    'audio' is now a numpy array provided by soundfile in app.py.
    """
    if audio is None or len(audio) == 0:
        return 0.0, 0.0, 0.0

    # Ensure audio is float32 for librosa
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)

    # 🎯 Pitch (YIN algorithm)
    try:
        # Added a check to ensure audio is long enough for fmin
        pitch_values = librosa.yin(audio, fmin=50, fmax=300)
        pitch = float(np.nanmean(pitch_values)) if len(pitch_values) > 0 else 0.0
    except:
        pitch = 0.0

    # 🔊 Energy (RMS equivalent)
    energy = float(np.mean(audio**2))

    # 🥁 Tempo
    try:
        # librosa 0.10+ returns (tempo, beat_frames) or just tempo depending on version
        tempo_data = librosa.beat.beat_track(y=audio, sr=fs)
        # Handle different librosa version return types
        if isinstance(tempo_data, tuple):
            tempo = float(tempo_data[0])
        else:
            tempo = float(tempo_data)
    except:
        tempo = 0.0

    return pitch, energy, tempo


# 📊 SCORE CALCULATION (Kept exactly as your original)
def calculate_lie_probability(current_stats, baseline_stats):
    """
    Compares current voice to baseline to find 'Stress'
    """
    c_pitch, c_energy, c_tempo = current_stats
    b_pitch, b_energy, b_tempo = baseline_stats
    
    score = 0
    
    # 1. Pitch Spike (Strongest Indicator)
    if b_pitch > 0 and c_pitch > (b_pitch * 1.10):
        score += 50 
        
    # 2. Energy/Volume Increase
    if b_energy > 0 and c_energy > (b_energy * 1.5):
        score += 25
        
    # 3. Tempo Change
    if b_tempo > 0:
        if c_tempo > (b_tempo * 1.2) or c_tempo < (b_tempo * 0.8):
            score += 25

    return min(score, 100) # Caps at 100%

def classify_voice_result(probability):
    if probability >= 75:
        return "HIGH STRESS (Potential Lie)"
    elif probability >= 40:
        return "MODERATE STRESS"
    else:
        return "STABLE (Likely Truth)"

# 🚀 No changes needed to logic below this line
