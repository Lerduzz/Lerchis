import sys, time, random
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication
from parchis_ui import Ui_VentanaJuego

class DadosWorker(QObject):
    finished = pyqtSignal(int, int)
    progress = pyqtSignal(int, int)

    def __init__(self, s1, s2):
        super().__init__()
        self.__s1 = s1
        self.__s2 = s2

    def run(self):
        count = 0
        while count < 15:
            self.__s1 = random.randint(1, 6)
            self.__s2 = random.randint(1, 6)
            count += 1
            self.progress.emit(self.__s1, self.__s2)
            time.sleep(0.05)
        self.finished.emit(self.__s1, self.__s2)


class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego() 
        self.ui.setupUi(self)
        self.ui.btnTirar.clicked.connect(self.tirarDados)
        self.__dado1 = 6
        self.__dado2 = 6
    
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.ui.cajaTablero.setFixedWidth(self.ui.cajaTablero.height())

    def tirarDados(self):
        self.ui.btnTirar.setEnabled(False)
        self.__dadosThread = QThread()
        self.__dadosWorker = DadosWorker(self.__dado1, self.__dado2)
        self.__dadosWorker.moveToThread(self.__dadosThread)
        self.__dadosThread.started.connect(self.__dadosWorker.run)
        self.__dadosWorker.finished.connect(self.__dadosThread.quit)
        self.__dadosWorker.finished.connect(self.__dadosWorker.deleteLater)
        self.__dadosThread.finished.connect(self.__dadosThread.deleteLater)
        self.__dadosWorker.progress.connect(self.mostrarDados)
        self.__dadosWorker.finished.connect(self.onDadosGirados)        
        self.__dadosThread.start()

    def mostrarDados(self, s1, s2):
        self.ui.dado1.setStyleSheet(f'border-image: url(:/dados/dado{s1}.png) 0 0 0 0 stretch stretch;')
        self.ui.dado2.setStyleSheet(f'border-image: url(:/dados/dado{s2}.png) 0 0 0 0 stretch stretch;')

    def onDadosGirados(self, s1, s2):
        self.__dado1 = s1
        self.__dado2 = s2
        self.ui.btnTirar.setEnabled(True)


app = QApplication([])
application = Ventana()
application.show()
sys.exit(app.exec())