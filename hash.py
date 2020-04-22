from PIL import Image
import imagehash, json
from imagehash import hex_to_hash
import numpy as np
from scipy import signal
from pydub import AudioSegment

weight = 0.8

audioFile1 = AudioSegment.from_mp3("Songs/Adele_Million_Years_Ago_10.mp3")[:60000]
songData1 = np.array(audioFile1.get_array_of_samples())
sampleRate1 = audioFile1.frame_rate
song1DataType = songData1.dtype

audioFile2 = AudioSegment.from_mp3("Songs/ImagineDragons_natural_10.mp3")[:60000]
songData2 = np.array(audioFile2.get_array_of_samples())
sampleRate2 = audioFile2.frame_rate

audioFile3 = AudioSegment.from_mp3("Songs/Adele_Million_Years_Ago_10_music.mp3")[:60000]
songData3 = np.array(audioFile3.get_array_of_samples())
sampleRate3 = audioFile2.frame_rate

# output = (weight*songData1 + (1.0-weight)*songData2).astype('int16')
output = (weight*songData1 + (1.0-weight)*songData2).astype(song1DataType)
print("output: \n", output)

sampleFreqs1, sampleTime1, colorMesh1 = signal.spectrogram(songData1, fs=sampleRate1, window='hann')
sampleFreqs2, sampleTime2, colorMesh2 = signal.spectrogram(songData2, fs=sampleRate2, window='hann')
sampleFreqs3, sampleTime3, colorMesh3 = signal.spectrogram(songData3, fs=sampleRate3, window='hann')
sampleFreqs4, sampleTime4, colorMesh4 = signal.spectrogram(output, fs=sampleRate3, window='hann')


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

