import librosa
import numpy as np
from scipy.signal import find_peaks, spectrogram


def get_dominant_frequency_autocorrelation(audio_data, sampling_rate):
    # Calcular la autocorrelación de la señal
    autocorrelation = np.correlate(audio_data, audio_data, mode='full')

    # Limitar la autocorrelación a valores positivos
    autocorrelation = autocorrelation[len(autocorrelation) // 2:]

    # Encontrar el primer pico en la autocorrelación (excluyendo el pico en 0)
    peaks, _ = find_peaks(autocorrelation, height=0.01)  # Ajusta el umbral según tu caso

    # Calcular la frecuencia fundamental
    if len(peaks) > 0:
        primer_pico = peaks[0]
        frecuencia_fundamental = sampling_rate / primer_pico
    else:
        # En caso de que no se encuentre ningún pico, retornar None o un valor predeterminado
        frecuencia_fundamental = None

    return frecuencia_fundamental

def get_dominant_frequency_fft(data, sampling_rate):
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data))
    peak_coefficient = np.argmax(np.abs(fft_data))
    peak_freq = freqs[peak_coefficient]

    return abs(peak_freq * sampling_rate)


def get_dominant_frequency_lowest_freq(data, sampling_rate):
    # Calcular la STFT (Transformada de Fourier de corto plazo)
    stft = np.abs(librosa.stft(data))
    intensity_threshold = np.mean(stft[:, 0])
    # print(m)
    # Obtener las frecuencias correspondientes a cada bin de la STFT
    frequencies = librosa.fft_frequencies(sr=sampling_rate)
    # print(frequencies)

    # Calcular la suma de intensidades en cada bin de frecuencia
    intensity_sum = np.sum(stft, axis=1) / len(data)
    # print(intensity_sum)

    peaks = []
    for i in range(len(intensity_sum)):
        if intensity_sum[i] > intensity_threshold and frequencies[i] > 100:
            peaks.append([intensity_sum[i], frequencies[i]])
    print(peaks)

    if peaks:
        # Obtener la frecuencia más grave que supere el umbral de intensidad
        lowest_freq_above_threshold = peaks[0][1]
    else:
        lowest_freq_above_threshold = 1

    return lowest_freq_above_threshold


def calculate_intensity_threshold(intensity_sum, percentile):
    # Ordenar la lista de intensidades en orden descendente
    sorted_intensity = sorted(intensity_sum, reverse=True)

    # Calcular el índice correspondiente al percentil
    index_percentile = int(len(sorted_intensity) * percentile)

    # Obtener el umbral de intensidad en ese percentil
    intensity_threshold = sorted_intensity[index_percentile]

    return intensity_threshold

def get_dominant_frequency_lowest_freq2(data, sampling_rate):
    # Calcular la FFT (Transformada de Fourier)
    fft_result = np.fft.fft(data)
    fft_magnitude = np.abs(fft_result)

    # Obtener las frecuencias correspondientes a cada bin de la FFT
    num_samples = len(data)
    frequencies = np.abs(np.fft.fftfreq(num_samples, 1 / sampling_rate))
    # Calcular la suma de intensidades en cada bin de frecuencia
    intensity_sum = (fft_magnitude / num_samples) ** 4

    # Definir un umbral de intensidad (puedes ajustar este valor según tus necesidades)
    intensity_threshold = calculate_intensity_threshold(intensity_sum, 0.25)
    print("##@#@@#@#@THRESHOLD", intensity_threshold )

    peaks = []
    for i in range(len(intensity_sum)):
        if intensity_sum[i] > intensity_threshold and frequencies[i] > 125:
            peaks.append([intensity_sum[i], frequencies[i]])

    if peaks:
        # Obtener la frecuencia más grave que supere el umbral de intensidad
        lowest_freq_above_threshold = peaks[0][1]
    else:
        lowest_freq_above_threshold = 1

    return lowest_freq_above_threshold


def get_dominant_frequency(data, sampling_rate):

    freq1 = librosa.yin(data, fmin=100, fmax=2000, sr=sampling_rate)
    #freq2 = get_dominant_frequency_autocorrelation(data,sampling_rate)
    print(f"FREQUENCIES: {freq1}, ")

    return np.mean(freq1)#el autocorrelation se columpia en los inicios, threshold consultado con la universidad de mis cojones 33
