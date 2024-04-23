import sys, time, random, qdarkstyle
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
        self.__turno = 0
        self.__fichas = [
            self.ui.ficha00, self.ui.ficha01, self.ui.ficha02, self.ui.ficha03,
            self.ui.ficha10, self.ui.ficha11, self.ui.ficha12, self.ui.ficha13,
            self.ui.ficha20, self.ui.ficha21, self.ui.ficha22, self.ui.ficha23,
            self.ui.ficha30, self.ui.ficha31, self.ui.ficha32, self.ui.ficha33
        ]
        self.__casas = [
            [self.ui.ficha00, self.ui.ficha01, self.ui.ficha02, self.ui.ficha03],
            [self.ui.ficha10, self.ui.ficha11, self.ui.ficha12, self.ui.ficha13],
            [self.ui.ficha20, self.ui.ficha21, self.ui.ficha22, self.ui.ficha23],
            [self.ui.ficha30, self.ui.ficha31, self.ui.ficha32, self.ui.ficha33]
        ]
    
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.resizeAll()
        self.relocateAll()

    def resizeAll(self):
        h = self.ui.cajaTablero.height()
        self.ui.cajaTablero.setFixedWidth(h)
        fH = 50 * h // 950
        for f in self.__fichas:
            f.setFixedWidth(fH)
            f.setFixedHeight(fH)
        
    def relocateAll(self):
        h = self.ui.cajaTablero.height()
        hCasa = 250 * h // 950
        hFicha = 50 * h // 950
        for i in range(4):
            casaX = (0 if i == 0 or i == 1 else 700) * h // 950
            casaY = (0 if i == 0 or i == 3 else 700) * h // 950
            for j in range(4):
                p1 = hCasa // 2 - hFicha - hFicha // 2
                p2 = hCasa // 2 + hFicha // 2
                self.__casas[i][j].move(casaX + (p1 if j == 0 or j == 1 else p2), casaY + (p1 if j == 0 or j == 3 else p2))

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
        self.ui.dado1.setStyleSheet(f'border-image: url(:/dados/dado{self.__turno}{s1}.png) 0 0 0 0 stretch stretch;')
        self.ui.dado2.setStyleSheet(f'border-image: url(:/dados/dado{self.__turno}{s2}.png) 0 0 0 0 stretch stretch;')

    def onDadosGirados(self, s1, s2):
        self.__dado1 = s1
        self.__dado2 = s2
        self.mostrarDados(s1, s2)
        # TODO: Esto es una prueba, no va en este lugar.
        self.ui.btnTirar.setEnabled(True)
        self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
        


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
application = Ventana()
application.show()
sys.exit(app.exec())