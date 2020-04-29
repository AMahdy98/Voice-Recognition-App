from helpers import createPerceptualHash
from Spectrogram import spectrogram
import loader
import json

def updateDB(filePath:str, mode: str = "a"):
    d = {}

    for audFile, path in loader.loadPath(filePath):
        data, rate = loader.mp3ToData(path, 60000)
        _, _, mesh = spectrogram()._spectrogram(data, rate)

        _, _, mcc = spectrogram().spectralFeatures(data, mesh, rate)
        spectrohash = createPerceptualHash(mesh)
        mcchash = createPerceptualHash(mcc)

        d.update({audFile: {"spectrohash": spectrohash, "mcc": mcchash}})
        print("%s is hashed" % audFile)

    with open("db.json", mode) as outfile:
        json.dump(d, outfile, indent="\n")


def readJson(file):
    with open(file) as jsonFile:
        data = json.load(jsonFile)
    for song in data:
        yield song, data[song]


if __name__ == '__main__':
    # updateDB("Songs", "a")
    for i in readJson("db.json"):
        print(i)
