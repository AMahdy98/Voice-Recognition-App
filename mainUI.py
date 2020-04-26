import UI as ui
from PyQt5 import QtWidgets
import logging

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
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)


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
