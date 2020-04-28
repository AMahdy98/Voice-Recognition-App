from helpers import *
from imagehash import hex_to_hash

# Load Songs
song1 = loadSong("Songs/Adele_Million_Years_Ago_10.mp3", 60000)
song2 = loadSong("Songs/ImagineDragons_natural_10.mp3", 60000)
song3 = loadSong("Songs/Spacetoon_remi_11.mp3", 60000)
song4 = loadSong("Songs/Adele_Million_Years_Ago_10_music.mp3", 60000)
song5 = loadSong("Songs/Adele_Million_Years_Ago_10_vocals.mp3", 60000)

# Mix 2 songs -> Create Spectrogram -> Create Hash
mixedSong = mixSongs(song1['data'], song2['data'], w=0.8)
sampleFrequency, sampleTime, colorMesh = signal.spectrogram(mixedSong, fs=song1['sRate'], window='hann')
hashMix = createPerceptualHash(colorMesh)

original = (song4['data'] + song5['data']).astype('int16')
sampleFrequency2, sampleTime2, colorMesh2 = signal.spectrogram(original, fs=song1['sRate'], window='hann')
hashMix2 = createPerceptualHash(colorMesh2)

diff1 = hex_to_hash(song1['spectrogram_Hash']) - hex_to_hash(hashMix)
diff2 = hex_to_hash(song2['spectrogram_Hash']) - hex_to_hash(hashMix)
diff3 = hex_to_hash(song3['spectrogram_Hash']) - hex_to_hash(hashMix)
diff4 = hex_to_hash(song4['spectrogram_Hash']) - hex_to_hash(hashMix)
diff5 = hex_to_hash(song1['spectrogram_Hash']) - hex_to_hash(song3['spectrogram_Hash'])
diff6 = hex_to_hash(song2['spectrogram_Hash']) - hex_to_hash(song3['spectrogram_Hash'])
diff7 = hex_to_hash(song1['spectrogram_Hash']) - hex_to_hash(hashMix2)

diff1New = mapRanges(diff1, 0, 255, 0, 1)
diff2New = mapRanges(diff2, 0, 255, 0, 1)
diff3New = mapRanges(diff3, 0, 255, 0, 1)
diff4New = mapRanges(diff4, 0, 255, 0, 1)
diff5New = mapRanges(diff5, 0, 255, 0, 1)
diff6New = mapRanges(diff6, 0, 255, 0, 1)
diff7New = mapRanges(diff7, 0, 255, 0, 1)

# Print the results
print(f'''
hash1: {song1['spectrogram_Hash']}
hash2: {song2['spectrogram_Hash']}
hash3: {song3['spectrogram_Hash']}
hash4: {song4['spectrogram_Hash']}
hash5: {song5['spectrogram_Hash']}
0.8: {song1['name']}
0.2: {song2['name']}
mixHash: {hashMix}

Difference {song1['name']} and Mix = {diff1}
Difference {song2['name']} and Mix = {diff2}
Difference {song3['name']} and Mix = {diff3}
Difference {song4['name']} and Mix = {diff4}

Similarity of {song1['name']} with the mix = {(1-diff1New)*100}%
Similarity of {song2['name']} with the mix = {(1-diff2New)*100}%
Similarity of {song3['name']} with the mix = {(1-diff3New)*100}%
Similarity of {song4['name']} with the mix = {(1-diff4New)*100}%

Difference {song1['name']} with {song3['name']} = {diff5}
Similarity = {(1-diff5New)*100}%

Difference {song2['name']} with {song3['name']} = {diff6}
Similarity = {(1-diff6New)*100}%

Difference {song1['name']} with its (music+vocals) = {diff7}
Similarity = {(1-diff7New)*100}%
''')

