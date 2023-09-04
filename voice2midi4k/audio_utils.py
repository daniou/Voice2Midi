import librosa


def get_fundamental_frequencies(data, sr):
    freqs = librosa.yin(data, fmin=100, fmax=2000, sr=sr)
    print(f"FREQUENCIES: {freqs}")

    return freqs
