import sys, os
from PyQt5.QtWidgets import QApplication
import signal
from PyQt5.QtCore import QTimer
from MainController import MainController
from ClassMainGuiManager import MainGUIManager
from main_ui import Ui_MainWindow

class MainApplication(QApplication):
    app_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
    def __init__(self,sys_argv):
        QApplication.__init__(self, sys_argv)
        self.imagesDirHSV = "../InputHSV/"
        self.imagesDirProcess = "../InputProcess/"
        self.mainController = MainController(self.imagesDirHSV,self.imagesDirProcess,self.app_dir)
        self.maingui_manager = MainGUIManager(self.mainController ,self.app_dir)
        self.maingui_manager.show()
        

        return

app_id = "MainApplication"


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()
    os.system("pkill -f " + app_id)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler) #SIGINT es ctrl+c
    app = MainApplication(sys.argv)


    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)


    sys.exit(app.exec_())
