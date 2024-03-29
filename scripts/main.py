import librosa
import audiomentations as am 
import pandas as pd
import numpy as np
import tensorflow as tf

from audio_parser import split_audio
#commentario prueba
#Global Variables
SAMPLES     = 500 #Number of modified audios per trigger
SR          = 5000 #Sample Rate
ITERACIONES = 10 #Iteraciones que hace la IA


FILES_PATH          = "../Audios/pums/"
CROPPED_AUDIOS_PATH = "../Cropped_Audios/"
CROPPED_NO_PUMS     = CROPPED_AUDIOS_PATH+"no_pums/"
CROPPED_PUMS        = CROPPED_AUDIOS_PATH+"pums/"
CSVS                = "../csvs/"
#Record Triggers
def recordTriggers():
    data, _ = librosa.load(FILES_PATH+"1.wav",sr=SR,duration=1)
    #print(data)
    return [data]

#Audio Augmentations
augment_raw_audio = am.Compose(
    [
        am.AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.8),
        am.PitchShift(min_semitones=-2, max_semitones=1, p=0.7),
        am.AddShortNoises(CROPPED_NO_PUMS,p=1),
        am.TimeStretch(0.8,1.2,leave_length_unchanged=True,p=0.9),
        am.PolarityInversion(p=0.5),
        am.Shift(min_fraction=-0.3,max_fraction=0.3,p=0.8)
    ]
)

#Generate Modulation
def generateModulations(sounds):
    modulations = []
    for sound in sounds:
        for i in range(SAMPLES):
            aug_sound = augment_raw_audio(sound,SR)
            modulations.append(aug_sound)
    #print(modulations)
    return modulations

#Extract Features
def extractFeatures(sounds):
    dataset = pd.DataFrame()
    for sound in sounds:
        #CARGAR ARCHIVO y SACAR FOURIER
        S, phase = librosa.magphase(librosa.stft(y=sound))
        # #[CRHOMAGRAMA]
        chroma               = librosa.feature.chroma_stft(y=sound,sr=SR)
        # #[SPECTRAL CENTROID]
        spectralCentroid     = librosa.feature.spectral_centroid(y=sound,sr=SR)
        # #[SPECTRAL BANDWIDTH]
        spectralBandwidth    = librosa.feature.spectral_bandwidth(y=sound,sr=SR)
        # #[SPECTRAL ROLL OFF]
        spectralRolloff      = librosa.feature.spectral_rolloff(y=sound,sr=SR, roll_percent=0.99)
        spectralRolloff_min  = librosa.feature.spectral_rolloff(y=sound, sr=SR,roll_percent=0.01)
        #[SPECTRAL ZERO CROSSING]
        spectralZeroCrossing = librosa.feature.zero_crossing_rate(y=sound,frame_length=SR)
        # #[mfcc]
        mfccs = librosa.feature.mfcc(y=sound,sr=SR)
        mfccs_scaled = [np.mean(feature) for feature in mfccs]
        # MONTA DATAFRAME CON LOS HEADERS CORRESPONDIENTES
        #como el mfccs tiene mas de un componente lo descomponemos en varias columnas
        mfccs_header = []
        for i in range(len(mfccs_scaled)):
            mfccs_header.append("Mfcc"+str(i))

        dataset=dataset.append([[1,np.mean(chroma),np.mean(spectralCentroid),np.mean(spectralBandwidth),np.mean(spectralRolloff),np.mean(spectralRolloff_min),np.mean(spectralZeroCrossing)]+mfccs_scaled])
    return dataset

#Load CSV file with non-trigger features
def loadNoTriggerFeatures(path):
    df = pd.read_csv(path, header=None,index_col=False)
    df = df.drop([0], axis=1)
    df = df.drop([0], axis=0)

    #Reset columns index
    df.columns = range(df.columns.size)
    return df


#Generate Dataset
def generateDataset(triggers):
    t  = extractFeatures(triggers)
    nt = loadNoTriggerFeatures(CSVS+"no_trigger_features.csv")
    # dataset = pd.concat([tf,ntf], ignore_index=True)
    dataset  = t.append(nt,ignore_index=True)
    features = dataset.iloc[: , 1:]
    target   = dataset.iloc[: , 0:1]
    features = np.array(features).astype(np.float32)
    target   = np.array(target).astype(np.float32)
    return features,target
    
#Create AI Model
def createModel(features,target):
    #print("RUNNING createModel")
    print(type(features)," ",type(target))
    # features.to_csv("f.csv")
    # target.to_csv("t.csv")
    print(features)
    tf.convert_to_tensor(features, dtype=tf.float32) #import data as tensor
    tf.convert_to_tensor(target, dtype=tf.float32)

    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(features)

    #Create model
    model = tf.keras.Sequential([
        normalizer,
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])
    #Train Model
    model.fit(features, target, epochs=ITERACIONES)
    
    #Add Last layer to normalize the output
    export_model = tf.keras.Sequential([
    model,
    tf.keras.layers.Activation('sigmoid')
    ])

    export_model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy'])
    return export_model

def extractData(sound):
    data = extractFeatures(sound)
    features = data.iloc[: , 1:]
    features = np.array(features).astype(np.float32)
    return features

def isPum(sound,model):
    soundFeatures = extractData(sound)
    result = model.predict(soundFeatures)
    if(result > 0.5):
        return True
    else:
        return False
    

#MAIN
triggers           = recordTriggers()
modulated_triggers = generateModulations(triggers)
features, target   = generateDataset(modulated_triggers)
model              = createModel(features,target)

chunks = split_audio("../Audios/no_pums/TERROR EN DISCOTECAS EUROPEAS POR UNA OLEADA DE CHICAS PINCHADAS CON JERINGUILLAS DURANTE LA FIESTA.wav")
for chunk in chunks:
    print("El chunk es trigger: ",isPum([chunk],model))
