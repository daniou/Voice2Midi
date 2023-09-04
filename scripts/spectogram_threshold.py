import librosa
import matplotlib.pyplot as plt
import numpy as np


def generate_spectrogram(audio_file, output_file, intensity_threshold):
    # Cargar el archivo de audio
    audio_data, sample_rate = librosa.load(audio_file, sr=8000)
    print(audio_data, sample_rate)

    # Calcular el espectrograma
    _, _, Sxx, _ = plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')

    # Aplicar umbral a la matriz del espectrograma
    Sxx[Sxx < intensity_threshold] = 0

    # Obtener los límites de los ejes x e y después de aplicar el umbral
    xlim = plt.xlim()
    ylim = plt.ylim()

    # Plotear el espectrograma modificado
    plt.imshow(10 * np.log10(Sxx), cmap='viridis', aspect='auto', origin='lower', extent=[*xlim, *ylim])
    plt.colorbar(format='%+2.0f dB')  # Agrega una barra de colores
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.title('Espectrograma de Audio')

    # Guardar el espectrograma como una imagen
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()


# Llamar a la función para generar y guardar el espectrograma
audio_file = "audio2.wav"
output_image_file = "spectrogram.png"
intensity_threshold = 0.1  # Ajusta este valor según tu umbral de intensidad deseado
generate_spectrogram(audio_file, output_image_file, intensity_threshold)
