from helpers import *
from math import ceil

hammingDifferences = []
feature1Differences = []
feature2Differences = []
feature3Differences = []
similarities = []
feature1Similarities = []
feature2Similarities = []
feature3Similarities = []
avgSimilaritiesAll = []
avgSimilaritiesF3 = []
weight = 0.8

# Load Songs
song1 = loadSong("Songs/Adele_Million_Years_Ago_10.mp3", 60000)
song2 = loadSong("Songs/ImagineDragons_natural_10.mp3", 60000)
song3 = loadSong("Songs/Birdy_strange_birds_10.mp3", 60000)
song4 = loadSong("Songs/Spacetoon_remi_11.mp3", 60000)
song5 = loadSong("Songs/Adele_Million_Years_Ago_10_music.mp3", 60000)
song6 = loadSong("Songs/Adele_Million_Years_Ago_10_vocals.mp3", 60000)
songs = [song1, song2, song3, song4, song5, song6]

# Mix 2 songs -> Create Spectrogram -> Create Hash
mixedSong = mixSongs(song1['data'], song2['data'], w=weight)
sampleFrequency, sampleTime, colorMesh = signal.spectrogram(mixedSong, fs=song1['sRate'], window='hann')
hashMix = createPerceptualHash(colorMesh)
f1HashMix = createPerceptualHash(l.feature.spectral_centroid(y= mixedSong, S=colorMesh, sr=song1['sRate'], window = 'hann'))
f2HashMix = createPerceptualHash(l.feature.spectral_rolloff(y= mixedSong, S=colorMesh, sr=song1['sRate'], window = 'hann'))
f3HashMix = createPerceptualHash(l.feature.melspectrogram(y= mixedSong, S=colorMesh, sr=song1['sRate'], window = 'hann'))

original = (song5['data'] + song6['data']).astype(song5['dType'])
sampleFrequency2, sampleTime2, colorMesh2 = signal.spectrogram(original, fs=song1['sRate'], window='hann')
hashMix2 = createPerceptualHash(colorMesh2)
f1HashMix2 = createPerceptualHash(l.feature.spectral_centroid(y= original, S=colorMesh2, sr=song5['sRate'], window = 'hann'))
f2HashMix2 = createPerceptualHash(l.feature.spectral_rolloff(y= original, S=colorMesh2, sr=song5['sRate'], window = 'hann'))
f3HashMix2 = createPerceptualHash(l.feature.melspectrogram(y= original, S=colorMesh2, sr=song5['sRate'], window = 'hann'))

# Calculate Hamming Distance and Map the values
# For the spectrogram
for i in range(4):
    hammingDifferences.append(getHammingDistance(hash1=songs[i]['spectrogram_Hash'], hash2=hashMix))
    similarities.append(mapRanges(hammingDifferences[i], 0, 255, 0, 1))

# For the spectral_centroid feature
for i in range(4):
    feature1Differences.append(getHammingDistance(hash1=songs[i]['spectral_centroid_Hash'], hash2=f1HashMix))
    feature1Similarities.append(mapRanges(feature1Differences[i], 0, 255, 0, 1))

# For the spectral_rolloff feature
for i in range(4):
    feature2Differences.append(getHammingDistance(hash1=songs[i]['spectral_rolloff_Hash'], hash2=f2HashMix))
    feature2Similarities.append(mapRanges(feature2Differences[i], 0, 255, 0, 1))

# For the melspectrogram feature
for i in range(4):
    feature3Differences.append(getHammingDistance(hash1=songs[i]['melspectrogram_Hash'], hash2=f3HashMix))
    feature3Similarities.append(mapRanges(feature3Differences[i], 0, 255, 0, 1))

# hammingDifferences.append(getHammingDistance(hash1=songs[0]['spectrogram_Hash'], hash2=hashMix2))
# similarities.append(mapRanges(hammingDifferences[4], 0, 255, 0, 1))
# feature1Similarities.append(mapRanges(feature1Differences[4], 0, 255, 0, 1))
# feature2Similarities.append(mapRanges(feature2Differences[4], 0, 255, 0, 1))
# feature3Similarities.append(mapRanges(feature3Differences[4], 0, 255, 0, 1))

# # Check Original Mix Similarity with Features
# f1Diff = getHammingDistance(hash1=songs[0]['spectral_centroid_Hash'], hash2=f1HashMix2)
# f2Diff = getHammingDistance(hash1=songs[0]['spectral_rolloff_Hash'], hash2=f2HashMix2)
# f3Diff = getHammingDistance(hash1=songs[0]['melspectrogram_Hash'], hash2=f3HashMix2)
# f1DiffMap = mapRanges(f1Diff, 0, 255, 0, 1)
# f2DiffMap = mapRanges(f2Diff, 0, 255, 0, 1)
# f3DiffMap = mapRanges(f3Diff, 0, 255, 0, 1)

# Print the results
print(f'''

hash1 (Adele)  : {song1['spectral_centroid_Hash']}
hash2 (Imagine): {song2['spectral_centroid_Hash']}
hash3 (Birdy)  : {song3['spectral_centroid_Hash']}
hash4 (Remi)   : {song4['spectral_centroid_Hash']}
{weight}: {song1['name']}
{ceil((1-weight)*10)/10}: {song2['name']}
mixHash: {hashMix}

---- Checking Using Spectrogram Hashing ----
Difference {song1['name']} and Mix = {hammingDifferences[0]}
Difference {song2['name']} and Mix = {hammingDifferences[1]}
Difference {song3['name']} and Mix = {hammingDifferences[2]}
Difference {song4['name']} and Mix = {hammingDifferences[3]}

Similarity of {song1['name']} with the mix = {(1-similarities[0])*100}%
Similarity of {song2['name']} with the mix = {(1-similarities[1])*100}%
Similarity of {song3['name']} with the mix = {(1-similarities[2])*100}%
Similarity of {song4['name']} with the mix = {(1-similarities[3])*100}%
''')
# Difference {song1['name']} with its (music+vocals) = {hammingDifferences[4]}
# Similarity = {(1-similarities[4])*100}%

print(f'''
---- Checking Using spectral_centroid Hashing ----
hash1: {song1['spectral_centroid_Hash']}
hash2: {song2['spectral_centroid_Hash']}
hash3: {song3['spectral_centroid_Hash']}
hash4: {song4['spectral_centroid_Hash']}

Difference {song1['name']} and Mix = {feature1Differences[0]}
Difference {song2['name']} and Mix = {feature1Differences[1]}
Difference {song3['name']} and Mix = {feature1Differences[2]}
Difference {song4['name']} and Mix = {feature1Differences[3]}

Similarity of {song1['name']} with the mix = {(1-feature1Similarities[0])*100}%
Similarity of {song2['name']} with the mix = {(1-feature1Similarities[1])*100}%
Similarity of {song3['name']} with the mix = {(1-feature1Similarities[2])*100}%
Similarity of {song4['name']} with the mix = {(1-feature1Similarities[3])*100}%
''')

print(f'''
---- Checking Using spectral_rolloff Hashing ----
hash1: {song1['spectral_rolloff_Hash']}
hash2: {song2['spectral_rolloff_Hash']}
hash3: {song3['spectral_rolloff_Hash']}
hash4: {song4['spectral_rolloff_Hash']}

Difference {song1['name']} and Mix = {feature2Differences[0]}
Difference {song2['name']} and Mix = {feature2Differences[1]}
Difference {song3['name']} and Mix = {feature2Differences[2]}
Difference {song4['name']} and Mix = {feature2Differences[3]}

Similarity of {song1['name']} with the mix = {(1-feature2Similarities[0])*100}%
Similarity of {song2['name']} with the mix = {(1-feature2Similarities[1])*100}%
Similarity of {song3['name']} with the mix = {(1-feature2Similarities[2])*100}%
Similarity of {song4['name']} with the mix = {(1-feature2Similarities[3])*100}%
''')

print(f'''
---- Checking Using melspectrogram Hashing ----
hash1: {song1['melspectrogram_Hash']}
hash2: {song2['melspectrogram_Hash']}
hash3: {song3['melspectrogram_Hash']}
hash4: {song4['melspectrogram_Hash']}

Difference {song1['name']} and Mix = {feature3Differences[0]}
Difference {song2['name']} and Mix = {feature3Differences[1]}
Difference {song3['name']} and Mix = {feature3Differences[2]}
Difference {song4['name']} and Mix = {feature3Differences[3]}

Similarity of {song1['name']} with the mix = {(1-feature3Similarities[0])*100}%
Similarity of {song2['name']} with the mix = {(1-feature3Similarities[1])*100}%
Similarity of {song3['name']} with the mix = {(1-feature3Similarities[2])*100}%
Similarity of {song4['name']} with the mix = {(1-feature3Similarities[3])*100}%
''')

# Calculate the average of spectrogram hash and all features hashes
for i in range(4):
    avg = (hammingDifferences[i]+feature1Differences[i]+feature2Differences[i]+feature3Differences[i])/4
    avgMap = mapRanges(avg, 0, 255, 0, 1)
    result = (1 - avgMap) * 100
    avgSimilaritiesAll.append(result)

print(f'''
---- Checking Using Average Of (Spectrogram + All Features) Hashing ----
Similarity of {song1['name']} with the mix = {avgSimilaritiesAll[0]}%
Similarity of {song2['name']} with the mix = {avgSimilaritiesAll[1]}%
Similarity of {song3['name']} with the mix = {avgSimilaritiesAll[2]}%
Similarity of {song4['name']} with the mix = {avgSimilaritiesAll[3]}%
''')

# Calculate the average of spectrogram hash and melspectrogram feature
for i in range(4):
    avg = (hammingDifferences[i]+feature3Differences[i])/2
    avgMap = mapRanges(avg, 0, 255, 0, 1)
    result = (1 - avgMap) * 100
    avgSimilaritiesF3.append(result)

print(f'''
---- Checking Using Average Of (Spectrogram + melspectrogram Feature) Hashing ----
Similarity of {song1['name']} with the mix = {avgSimilaritiesF3[0]}%
Similarity of {song2['name']} with the mix = {avgSimilaritiesF3[1]}%
Similarity of {song3['name']} with the mix = {avgSimilaritiesF3[2]}%
Similarity of {song4['name']} with the mix = {avgSimilaritiesF3[3]}%
''')
