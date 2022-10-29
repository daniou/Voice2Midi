import librosa
import numpy as np

CHUNK = 1



def split_audio(path):
    data, _ =librosa.load("../Audios/pums/1.wav",sr=5000,duration=5)
    notpum, _ =librosa.load(path,sr=5000,duration=5)
    chunks = []
    data = np.concatenate((notpum,data,notpum))
    chunkSamples = (5000*CHUNK)
    print("(len-data: ",len(data),") / (chunkSamples: ",chunkSamples,") = ",len(data)/chunkSamples)
    samples = 0
    while samples < len(data):
        chunk = data[samples:min(samples+chunkSamples,len(data))]
        samples+=chunkSamples
        chunks.append(chunk)
    print("Longitud del chunks es: ",len(chunks))
    return chunks
