from scipy import signal
import json

class spectrogram():
    """
    Responsible for creating spectrograms for any .wav file
    implements the following:
    - reads a loaded wav file data and creates the associated spectrum
    - save the spectrum created in an arbitrary file
    """
    def __init__(self):
        """
        Class Initializer

        parameters
        ```````````
        - sampleFreqs : holds the sampled frequencies
        - sampleTime : holds the sampled time rates
        - colorMesh : holds the value (intenisty) of the frequency component
        - container : a dictionary used in the saved process
        """
        print("Initializing Spectrogram")
        self.sampleFreqs = None
        self.sampleTime = None
        self.colorMesh = None
        self.container = {}

    def __call__(self, songData: "numpy.ndarray", songSR: int, window:str, songName:str,
                 path:str = None, compressed: bool = False):
        """
        Caller function for the class which maintains all it's implemented methods

        parameters
        ```````````
        - songData: a numpy array of the read wav file
        - songSR : integer representing the sample rate
        - window : a str specifying the widow type used in creating the spectrogram
        - path : str if specified the file is saved in the given path
        - songName : the name of the file to be saved
        - compressed : if True only the color mesh will be saved
        """
        self._spectrogram(songData, songSR, window)
        print("spectrogram created")
        if path is None:
            self._saveFormat('', songName, compressed=compressed)
            print("saved in main directory .. ")
        else:
            self._saveFormat(path, songName, compressed=compressed)
        print("spectrogram saved")

    def _spectrogram(self, songData: "numpy.ndarray", songSampleRate:int, windowType: str):
        """
        Creates a Spectrogram of the given data

        parameters
        ``````````
        - songData : a numpy array of the read wav file
        - songSampleRate : integer representing the sample rate
        - windowType : a str specifying the widow type used in creating the spectrogram
        """
        if len(songData.shape) == 2:
            print("song is stereo")
            print("Converting ..")
            self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData[:, 0],
                                                                                   fs=songSampleRate, window=windowType)
        else:
            self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData,
                                                                                   fs=songSampleRate, window=windowType)

    def _saveFormat(self, folder:str, filename:str, compressed: bool = False):
        """
        Save the spectrum in a specified filename.json

        :parameters
        ```````````
        - folder : a path to the file location
        - filename : the file name
        - compressed : if True only the color mesh will be saved
        """
        if compressed:
            self.container = {"color_mesh": self.colorMesh.tolist()}
        else:
            self.container = {'sample_frequencies': self.sampleFreqs.tolist(),
                              "sample_time": self.sampleTime.tolist(),
                              "color_mesh": self.colorMesh.tolist()}

        with open(folder+filename+".json", 'w') as outfile:
            json.dump(self.container, outfile)


if __name__ == '__main__':
    # Basic Usage

    from scipy.io import wavfile
    sampleRate, songdata = wavfile.read("Adele_Million_Years_Ago_10.wav")
    spectrum = spectrogram()
    spectrum(songdata, sampleRate, window='hann', songName="test", compressed=True, path='tests/')



