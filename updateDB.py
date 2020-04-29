from helpers import createPerceptualHash
from Spectrogram import spectrogram
import loader
import json

def updateDB(filePath:str, fileOut:str, mode: str = "a"):
    d = {}

    for audFile, path in loader.loadPath(filePath):
        data, rate = loader.mp3ToData(path, 60000)
        _, _, mesh = spectrogram()._spectrogram(data, rate)

        _, _, mcc = spectrogram().spectralFeatures(data, mesh, rate)
        spectrohash = createPerceptualHash(mesh)
        mcchash = createPerceptualHash(mcc)

        d.update({audFile: {"spectrohash": spectrohash, "mcc": mcchash}})
        print("%s is hashed" % audFile)

    with open(fileOut+"db.json", mode) as outfile:
        json.dump(d, outfile, indent="\n")


def readJson(file):
    with open(file) as jsonFile:
        data = json.load(jsonFile)
    for song in data:
        yield song, data[song]


if __name__ == '__main__':
    import sys
    import warnings

    warnings.filterwarnings("ignore")

    if sys.argv[1] and sys.argv[2]:
        updateDB(sys.argv[1], sys.argv[2], "w")
    else:
        for i in readJson("db.json"):
            print(i)
            print("File paths not given")

    print("End of Script")
