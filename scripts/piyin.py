import librosa
import numpy as np

def yin_pitch_detection_librosa(file_path, fmin=100, fmax=2000):
    # Cargar archivo de audio
    y, sr = librosa.load(file_path)

    # Estimar el tono fundamental (F0) utilizando el algoritmo YIN
    f0 = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr)

    return f0

print(yin_pitch_detection_librosa("audio2.wav"))