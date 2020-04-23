from pydub import AudioSegment
import numpy as np

# Load into PyDub
songData = AudioSegment.from_wav("Adele_Million_Years_Ago_10.wav")
dataSlice = songData[:60000]
print("originalLength: ", len(songData))
samples = songData.get_array_of_samples()
print(type(samples))
samplesArray = np.array(samples)
print(type(samplesArray))
print(samplesArray)
print(songData.frame_rate)

# print("slicedLength: ", len(dataSlice))

# print(dataSlice.get_array_of_samples())
# dataSlice.export("adele60.mp3", format="mp3")

# Play the result
# play(songData)
