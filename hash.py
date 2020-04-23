from PIL import Image
import imagehash, json
from imagehash import hex_to_hash
import numpy as np
from scipy import signal
from pydub import AudioSegment

weight = 0.8

# Load Files
def loadAudioFile(filePath: str, fSeconds: float = None) -> dict:
    """
    Loads any audio file

    :param filePath: relative path of the file
    :param fSeconds: number of seconds you want to load, if not it will load all the file
    :return: Dictionary contains songName, pydub Object, array of the data, sample rate, dataType of the array
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
    }
    return songDictionary

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

song1 = loadAudioFile("Songs/Adele_Million_Years_Ago_10.mp3", 60000)
song2 = loadAudioFile("Songs/ImagineDragons_natural_10.mp3", 60000)
song3 = loadAudioFile("Songs/Adele_Million_Years_Ago_10_music.mp3", 60000)
mixedSong = mixSongs(song1['data'], song2['data'], w=0.8)

sampleFreqs1, sampleTime1, colorMesh1 = signal.spectrogram(song1['data'], fs=song1['sRate'], window='hann')
sampleFreqs2, sampleTime2, colorMesh2 = signal.spectrogram(song2['data'], fs=song2['sRate'], window='hann')
sampleFreqs3, sampleTime3, colorMesh3 = signal.spectrogram(song3['data'], fs=song3['sRate'], window='hann')
sampleFreqs4, sampleTime4, colorMesh4 = signal.spectrogram(mixedSong, fs=song1['sRate'], window='hann')


def createPerceptualHash(arrayData: "np.ndarray") -> str:
    """
    Creates a perceptual hash of the given data
    :param arrayData: an array contains the data to be hashed
    :return: a string describe the hashed array (could be converted to hex using hex_to_hash())
    """
    dataInstance = Image.fromarray(arrayData).convert('RGB')
    dataHash = imagehash.phash(dataInstance, hash_size=16)
    return dataHash.__str__()


hash1 = createPerceptualHash(colorMesh1)
hash2 = createPerceptualHash(colorMesh2)
hash3 = createPerceptualHash(colorMesh3)
hashMix = createPerceptualHash(colorMesh4)

hash1Hex = hex_to_hash(hash1)
hash2Hex = hex_to_hash(hash2)
hash3Hex = hex_to_hash(hash3)
hashMixHex = hex_to_hash(hashMix)

result1 = hash1Hex - hashMixHex
result2 = hash2Hex - hashMixHex
result3 = hash3Hex - hashMixHex
total = result1 + result2 + result3

print("hash1: ", hash1)
print("hash2: ", hash2)
print("hash3: ", hash3)
print("mixHash: ", hashMix)

print("diff hash1 and mix", hash1Hex - hashMixHex)
print("diff hash2 and mix", hash2Hex - hashMixHex)
print("diff hash3 and mix", hash3Hex - hashMixHex)

