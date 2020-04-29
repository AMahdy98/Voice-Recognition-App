import UI as ui
from PyQt5 import QtWidgets
import logging
from loader import mp3ToData
from functools import partial
from Spectrogram import spectrogram
from helpers import mixSongs, createPerceptualHash, getHammingDistance, mapRanges
from updateDB import readJson

class voiceRecognizer(ui.Ui_MainWindow):
    """
    Audio and Voice Recognition Application implements the following :

    - Creating a Spectral Hash for each Song/Audio in a huge database
    - Identifying new Audio/Sound Added to the application
    - Mixing different Audio/Sound with selected ratios and finding that bizarre output in the database
    """
    def __init__(self, starterWindow: QtWidgets.QMainWindow):
        # Initializer
        super(voiceRecognizer, self).setupUi(starterWindow)
        self.spectroHashKey = "spectrohash"  # Key used to get the spectrogram Hash
        self.melKey = "mcc"  # key used to get mel Hash
        self.audFiles = [None, None]  # List Containing both songs
        self.audRates = [None, None]  # List contains Songs Rates which must be equal
        self.lineEdits = [self.aud1Text, self.aud2Text]
        self.testHash = None  # The Mix output resulted hash
        self.audMix = None  # The Mix output resulted Audio File
        self.featureHash = None  # Holds the features extracted from Mix
        self.results = {}  # Holds the Results with each song
        self.songsPath = "Songs/"  # path to songs directory
        self.dbPath = "Database/db.json"  # path to database directory
        self.spectrogram = spectrogram()._spectrogram  # Spectrogram Extraction function
        self.extractFeatures = spectrogram().spectralFeatures  # Feature Extraction function
        self.loadBtns = [self.audLoad1, self.audLoad2]  # loading buttons collected
        self.logger = logging.getLogger()  # Logger maintainer
        self.logger.setLevel(logging.DEBUG)

        # CONNECTIONS
        for btn in self.loadBtns:
            btn.clicked.connect(partial(self.loadFile, btn.property("indx")))

        self.finderBtn.clicked.connect(self.__extract)

    def loadFile(self, indx):
        """
        Responsible for the following :

        - Showing a dialog for choosing desired file
        - Convert the loaded file into array and insert it in the system
        - load only the first minute of any song
        """
        self.statusbar.showMessage("Loading Audio File %s"%indx)
        print(indx)
        audFile, audFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File %s"%(indx),
                                                                                 filter="*.mp3")
        self.logger.debug("Audio File %s Loaded"%indx)

        # CHECK CONDITIONS
        if audFile == "":
            self.logger.debug("loading cancelled")
            self.statusbar.showMessage("Loading cancelled")
            pass
        else:
            self.logger.debug("starting extraction of data")
            audData, audRate = mp3ToData(audFile, 60000)
            self.logger.debug("extraction successful")
            self.audFiles[indx-1] = audData
            self.audRates[indx-1] = audRate
            self.lineEdits[indx-1].setText(audFile)
            self.statusbar.showMessage("Loading Done")
            self.logger.debug("Loading done")
            print(self.audFiles[indx-1])

    def __extract(self):
        """
        Responsible for the following :

        - Read the slider value and mix the loaded songs if any with the selected ratio
        - Extract the spectrogram of the resulted mix and it`s features
        - hash the resulted extractions
        """
        print("Slider Value is %s"%self.ratioSlider.value())
        self.statusbar.showMessage("Finding Matches ...")
        self.logger.debug("starting searching process")

        if (self.audFiles[0] is not None) and (self.audFiles[1] is not None):
            print("here")
            self.logger.debug("loaded two different songs ")
            self.audMix = mixSongs(self.audFiles[0], self.audFiles[1], w=self.ratioSlider.value()/100)
        else:
            print("here2")
            self.logger.debug("loaded only one song")
            if self.audFiles[0] is not None : self.audMix = self.audFiles[0]
            if self.audFiles[1] is not None: self.audMix = self.audFiles[1]

        self.logger.debug("starting Extraction")
        print(self.audFiles[0])

        self.testHash = createPerceptualHash(self.spectrogram(self.audMix, self.audRates[0])[-1])
        self.featureHash = createPerceptualHash(self.extractFeatures(self.audMix,
                                                                     self.spectrogram(self.audMix, self.audRates[0])[-1],
                                                                     self.audRates[0])[-1])
        self.__compareHash()

    def __compareHash(self):
        """
        Responsible for the following :

        - Reading the database's saved hashes
        - Compare the resulted hashesh with those saved in database
        """
        self.logger.debug("staring comparisons ... ")
        self.statusbar.showMessage("Loading results .. ")
        for songName, songHashes in readJson('db.json'):
            self.results.update({songName: mapRanges(getHammingDistance(songHashes[self.spectroHashKey],
                                                                        self.testHash), 0, 255, 0, 1)})
        print(self.results)


if __name__ == '__main__':
    import sys
    logging.basicConfig(filename="logs/logfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = voiceRecognizer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
