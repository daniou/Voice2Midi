import numpy as np
import librosa


def get_dominant_frequency_lowest_freq2(data, sampling_rate):
    # Calcular la FFT (Transformada de Fourier)
    fft_result = np.fft.fft(data)
    fft_magnitude = np.abs(fft_result)

    # Obtener las frecuencias correspondientes a cada bin de la FFT
    num_samples = len(data)
    frequencies = np.fft.fftfreq(num_samples, 1 / sampling_rate)

    # Calcular la suma de intensidades en cada bin de frecuencia
    intensity_sum = fft_magnitude / num_samples

    # Definir un umbral de intensidad (puedes ajustar este valor según tus necesidades)
    intensity_threshold = np.mean(intensity_sum)

    peaks = []
    for i in range(len(intensity_sum)):
        if intensity_sum[i] > intensity_threshold and frequencies[i] > 100:
            peaks.append([intensity_sum[i], frequencies[i]])

    if peaks:
        # Obtener la frecuencia más grave que supere el umbral de intensidad
        lowest_freq_above_threshold = peaks[0][1]
    else:
        lowest_freq_above_threshold = 1

    return lowest_freq_above_threshold



def calculate_yin_pitch(samples, samplerate, min_f0=100, max_f0=2000, threshold=0.0001):
    tau_max = int(samplerate / min_f0)
    tau_min = int(samplerate / max_f0)
    N = len(samples)

    # Cálculo de la diferencia de tonos (difference function)
    yin_diff = np.zeros(tau_max + 1)

    for tau in range(1, tau_max + 1):
        for j in range(tau, N):
            yin_diff[tau] += (samples[j] - samples[j - tau]) ** 2

    # Aplicar el umbral y encontrar el mínimo local
    tau_candidate = None

    for tau in range(tau_min, tau_max + 1):
        if yin_diff[tau] < threshold:
            if tau_candidate is None or yin_diff[tau] < yin_diff[tau_candidate]:
                tau_candidate = tau

    if tau_candidate:
        # Interpolación parabólica para encontrar la frecuencia fundamental
        if tau_candidate + 1 < tau_max:
            if yin_diff[tau_candidate + 1] < yin_diff[tau_candidate]:
                alpha = yin_diff[tau_candidate + 1]
            else:
                alpha = yin_diff[tau_candidate]
        else:
            alpha = yin_diff[tau_candidate]

        if tau_candidate - 1 > 1:
            if yin_diff[tau_candidate - 1] < alpha:
                alpha = yin_diff[tau_candidate - 1]

        f0 = samplerate / (tau_candidate + alpha / (yin_diff[tau_candidate] - alpha - yin_diff[tau_candidate + 1]))
        return f0
    else:
        return None


# Ejemplo de uso
if __name__ == "__main__":
    audio_path = 'audio2.wav'
    intensity_threshold = 0  # Ajusta el umbral de intensidad según tus necesidades

    audio, sr = librosa.load(audio_path, sr=8000)
    lowest_freq_above_threshold = calculate_yin_pitch(audio, sr)

    if lowest_freq_above_threshold is not None:
        print(f"Frecuencia más grave que supera el umbral: {lowest_freq_above_threshold} Hz")
    else:
        print("No se encontraron frecuencias que superen el umbral de intensidad.")
