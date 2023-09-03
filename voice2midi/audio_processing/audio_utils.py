import numpy as np
from scipy.signal import find_peaks


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


def get_dominant_frequency(data, sampling_rate):

    freq1 = get_dominant_frequency_fft(data,sampling_rate)
    #freq2 = get_dominant_frequency_autocorrelation(data,sampling_rate)
    print(f"FREQUENCIES: {freq1}, ")

    return freq1#el autocorrelation se columpia en los inicios, threshold consultado con la universidad de mis cojones 33
