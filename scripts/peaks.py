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


# Ejemplo de uso
if __name__ == "__main__":
    audio_path = 'audio2.wav'
    intensity_threshold = 0  # Ajusta el umbral de intensidad según tus necesidades

    audio, sr = librosa.load(audio_path, sr=None)
    lowest_freq_above_threshold = get_dominant_frequency_lowest_freq2(audio, sr)

    if lowest_freq_above_threshold is not None:
        print(f"Frecuencia más grave que supera el umbral: {lowest_freq_above_threshold} Hz")
    else:
        print("No se encontraron frecuencias que superen el umbral de intensidad.")
