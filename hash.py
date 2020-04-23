from PIL import Image
import imagehash, json
from imagehash import hex_to_hash
import numpy as np
from scipy import signal
from pydub import AudioSegment
import librosa as l


def loadAudioFile(filePath: str, fSeconds: float = None) -> dict:
    """
    Loads any audio file

    :param filePath: relative path of the file
    :param fSeconds: number of seconds you want to load, if not it will load all the file
    :return: Dictionary contains songName, array of the data, sample rate, dataType of the array
    """
    if fSeconds:
        audioFile = AudioSegment.from_mp3(filePath)[:fSeconds]
    else:
        audioFile = AudioSegment.from_mp3(filePath)
    songName = filePath.split('/')[-1]
    songData = np.array(audioFile.get_array_of_samples())
    sampleRate = audioFile.frame_rate
    songDataType = songData.dtype
    songDictionary = {
        "name": songName,
        "data": songData,
        "sRate": sampleRate,
        "dType": songDataType,
        "spectrogram_Hash": None,
        "spectral_centroid_Hash": None,
        "spectral_rolloff_Hash": None,
        "melspectrogram_Hash": None,
        "hammingDistance": None
    }
    return songDictionary


def _spectralFeatures(song: "np.ndarray"= None, S: "np.ndarray" = None, sr: int = 22050, window: str = 'hann'):
    """
    Calculates the Spectral Centroid of a given data or the data instantiated in the class

    Parameters
    -----------
    - song  : wav file array
    - S    : spectrogram readings
    - sr : sampling frequency default 22050
    - window: a string specifying the window applied default hann (see options)
    """
    specFeatures = [None, None, None]
    specFeatures[0] = l.feature.spectral_centroid(y= song, S=S, sr=sr, window = window)
    specFeatures[1] = l.feature.spectral_rolloff(y= song, S=S, sr=sr, window = window)
    specFeatures[2] = l.feature.melspectrogram(y= song, S=S, sr=sr, window = window)
    return specFeatures


def mixSongs(song1: np.ndarray, song2: np.ndarray, dType: str = 'int16', w: float = 0.5) -> np.ndarray:
    """
    Mixes 2 songs with the given weight
    :param song1: data array of the song1
    :param song2: data array of the song2
    :param dType: data type of the song
    :param w: weight (percentage) of song1
    :return array of the mixing songs
    """
    mixed = (w*song1 + (1.0-w)*song2).astype(dType)
    return mixed


def createPerceptualHash(arrayData: "np.ndarray") -> str:
    """
    Creates a perceptual hash of the given data
    :param arrayData: an array contains the data to be hashed
    :return: a string describe the hashed array (could be converted to hex using hex_to_hash())
    """
    dataInstance = Image.fromarray(arrayData).convert('RGB')
    dataHash = imagehash.phash(dataInstance, hash_size=16)
    return dataHash.__str__()


def loadSong(filePath: str, fSeconds: float = None) -> dict:
    """
    Loads any audio file, create a spectrogram, extract some features and hash them.

    :param filePath: relative path of the file
    :param fSeconds: number of seconds you want to load, if not it will load all the file
    :return: Dictionary contains songName, array of the data, sample rate, dataType of the array and the hashes
    """
    song = loadAudioFile(filePath, fSeconds)
    sampleFreqs, sampleTime, colorMesh = signal.spectrogram(song['data'], fs=song['sRate'], window='hann')
    features = _spectralFeatures(song=song['data'], S=colorMesh, sr=song['sRate'])
    song['spectrogram_Hash'] = createPerceptualHash(colorMesh)
    song['spectral_centroid_Hash'] = createPerceptualHash(features[0])
    song['spectral_rolloff_Hash'] = createPerceptualHash(features[1])
    song['melspectrogram_Hash'] = createPerceptualHash(features[2])
    return song

# Load Songs
song1 = loadSong("Songs/Adele_Million_Years_Ago_10.mp3", 60000)
song2 = loadSong("Songs/ImagineDragons_natural_10.mp3", 60000)
song3 = loadSong("Songs/Adele_Million_Years_Ago_10_music.mp3", 60000)
song4 = loadSong("Songs/Spacetoon_remi_11.mp3", 60000)

songs = [song1, song2, song3, song4]

# Mix 2 songs -> Create Spectrogram -> Create Hash
mixedSong = mixSongs(song1['data'], song2['data'], w=0.8)
sampleFreqs4, sampleTime4, colorMesh4 = signal.spectrogram(mixedSong, fs=song1['sRate'], window='hann')
hashMix = createPerceptualHash(colorMesh4)

# Summation of all hamming Distance
# Rule for Similarity Index: (1-hammingDistance/totalHashes)*100
totalHashes = 0
for song in songs:
    song['hammingDistance'] = hex_to_hash(song['spectrogram_Hash']) - hex_to_hash(hashMix)
    totalHashes += song['hammingDistance']

# Print the results
print("hash1: ", song1['spectrogram_Hash'])
print("hash2: ", song2['spectrogram_Hash'])
print("hash3: ", song3['spectrogram_Hash'])
print("hash4: ", song4['spectrogram_Hash'])
print("mixHash: ", hashMix)

print("diff hash1 and mix", hex_to_hash(song1['spectrogram_Hash']) - hex_to_hash(hashMix))
print("diff hash2 and mix", hex_to_hash(song2['spectrogram_Hash']) - hex_to_hash(hashMix))
print("diff hash3 and mix", hex_to_hash(song3['spectrogram_Hash']) - hex_to_hash(hashMix))
print("diff hash4 and mix", hex_to_hash(song4['spectrogram_Hash']) - hex_to_hash(hashMix))
print("total Hashes", totalHashes)

print(f"Similarity of song1 with the mix = {(1-song1['hammingDistance']/totalHashes)*100}%")
print(f"Similarity of song2 with the mix = {(1-song2['hammingDistance']/totalHashes)*100}%")
print(f"Similarity of song3 with the mix = {(1-song3['hammingDistance']/totalHashes)*100}%")
print(f"Similarity of song4 with the mix = {(1-song4['hammingDistance']/totalHashes)*100}%")
