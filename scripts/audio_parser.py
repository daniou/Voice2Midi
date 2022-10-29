import librosa

CHUNK = 1



def split_audio(path):
    data, _ =librosa.load("./testaudios/1_0.wav",sr=5000,duration=5)
    chunks=[]
    chunkSamples = (5000*CHUNK)
    while i < len(data)/chunkSamples:
        chunk = data[i:min(i+chunkSamples,len(data)-i)]
        i+=chunkSamples
        chunks.append(chunk)

    return chunks
