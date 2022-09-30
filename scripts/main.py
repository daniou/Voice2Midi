import librosa
import audiomentations as am 
import pandas as pd
import numpy as np

#Global Variables
SAMPLES = 500 #Number of modified audios per trigger
SR      = 5000 #Sample Rate

FILES_PATH = "./Audios/pums/"
CROPPED_AUDIOS_PATH = "./Cropped_Audios/"
CROPPED_NO_PUMS = CROPPED_AUDIOS_PATH+"no_pums/"
CROPPED_PUMS = CROPPED_AUDIOS_PATH+"pums/"

#Record Triggers
def recordTriggers():
    data, _ = librosa.load(FILES_PATH+"1.wav",sr=SR,duration=1)
    #print(data)
    return [data]

#Audio Augmentations POLLA la
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
        chroma = librosa.feature.chroma_stft(y=sound,sr=SR)
        # #[SPECTRAL CENTROID]
        spectralCentroid = librosa.feature.spectral_centroid(y=sound,sr=SR)
        # #[SPECTRAL BANDWIDTH]
        spectralBandwidth = librosa.feature.spectral_bandwidth(y=sound,sr=SR)
        # #[SPECTRAL ROLL OFF]
        spectralRolloff = librosa.feature.spectral_rolloff(y=sound,sr=SR, roll_percent=0.99)
        spectralRolloff_min = librosa.feature.spectral_rolloff(y=sound, sr=SR,roll_percent=0.01)
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

        dataset=dataset.append([1,np.mean(chroma),np.mean(spectralCentroid),np.mean(spectralBandwidth),np.mean(spectralRolloff),np.mean(spectralRolloff_min),np.mean(spectralZeroCrossing)]+mfccs_scaled)
    return dataset

#Load CSV file with non-trigger features
def loadNoTriggerFeatures(path):
    return pd.read_csv(path)


#Generate Dataset
def generateDataset(triggers):
    dataset = pd.DataFrame()
    dataset = dataset.append(extractFeatures(triggers))
    dataset = dataset.append(loadNoTriggerFeatures("no_trigger_features.csv"))
    features = dataset.iloc[: , 2:]
    target = dataset.iloc[: , 1:2]
    return features,target
    


#MAIN
triggers    = recordTriggers()
modulated_triggers = generateModulations(triggers)
features, target   = generateDataset(modulated_triggers)
print(target)
