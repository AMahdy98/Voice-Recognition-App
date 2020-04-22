from PIL import Image
import imagehash, json
from imagehash import hex_to_hash
import numpy as np
from scipy import signal
from pydub import AudioSegment

audioFile = AudioSegment.from_mp3("Songs/Adele_Million_Years_Ago_10.mp3")[:60000]
songData = np.array(audioFile.get_array_of_samples())
sampleRate = audioFile.frame_rate

sampleFreqs, sampleTime, colorMesh = signal.spectrogram(songData, fs=sampleRate, window='hann')


def createPerceptualHash(arrayData: "np.ndarray") -> str:
    """
    Creates a perceptual hash of the given data
    :param arrayData: an array contains the data to be hashed
    :return: a string describe the hashed array (could be converted to hex using hex_to_hash())
    """
    dataInstance = Image.fromarray(arrayData).convert('RGB')
    dataHash = imagehash.phash(dataInstance)
    return dataHash.__str__()


hash1 = createPerceptualHash(colorMesh)
hash2 = createPerceptualHash(colorMesh)
print(hash1)
print(hash2)

