import librosa
import matplotlib.pyplot as plt


def generate_spectrogram(audio_file, output_file):
    # Cargar el archivo de audio
    audio_data, sample_rate = librosa.load(audio_file, sr=8000)
    print(audio_data, sample_rate)

    # Calcular el espectrograma
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño de la figura
    plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
    plt.colorbar(format='%+2.0f dB')  # Agrega una barra de colores
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.title('Espectrograma de Audio')

    # Guardar el espectrograma como una imagen
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()


# Llamar a la función para generar y guardar el espectrograma
audio_file = "audio.wav"
output_image_file = "spectrogram.png"
generate_spectrogram(audio_file, output_image_file)
