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
        self.__caminos = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            # TODO: Diagonales [None, None],
        ]
        self.__posCaminos = [
            (250, 0,   0),
            (250, 50,  0),
            (250, 100, 0),
            (250, 150, 0),
            (250, 200, 0),
            (250, 250, 2),
            (250, 250, 2),
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
        # CASAS
        hCasa = 250 * h // 950
        hFicha = 50 * h // 950
        for i in range(len(self.__casas)):
            casaX = (0 if i == 0 or i == 1 else 700) * h // 950
            casaY = (0 if i == 0 or i == 3 else 700) * h // 950
            for j in range(len(self.__casas[i])):
                p1 = hCasa // 2 - hFicha - hFicha // 2
                p2 = hCasa // 2 + hFicha // 2
                if self.__casas[i][j] != None:
                    self.__casas[i][j].move(casaX + (p1 if j == 0 or j == 1 else p2), casaY + (p1 if j == 0 or j == 3 else p2))
        # CAMINOS
        hCasilla = 150 * h // 950
        for i in range(len(self.__caminos)):
            x, y, o = self.__posCaminos[i]
            for j in range(2):
                if self.__caminos[i][j] != None:
                    xR, yR = self.calcularPosicionCasilla(x, y, o, j, h, hCasilla, hFicha)
                    self.__caminos[i][j].move(xR, yR)

    def calcularPosicionCasilla(self, x, y, o, i, h, hC, hF):
        xR, yR = (0, 0)
        dX = x * h // 950
        dY = y * h // 950
        dP1 = hC // 2 - hF - hF // 10
        dP2 = hC // 2 + hF // 10
        if o == 0:
            xR = dX + dP1 if i == 0 else dX + dP2
            yR = dY
        elif o == 1:
            xR = dX
            yR = dY + dP1 if i == 0 else dY + dP2
        elif o == 2:
            xR = dX + hC // 2 - hF // 4 if i == 0 else dX + hC // 2 + hF // 2 + hF // 10
            yR = dY if i == 0 else dY + hF // 2
        return (xR, yR)


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
        # TODO: TEST: Relocate.
        self.moverFicha(self.__casas, 0, 0, self.__caminos, 0, 0)
        self.moverFicha(self.__casas, 2, 0, self.__caminos, 0, 1)
        self.moverFicha(self.__casas, 1, 0, self.__caminos, 1, 0)
        self.moverFicha(self.__casas, 3, 0, self.__caminos, 1, 1)
        self.moverFicha(self.__casas, 0, 1, self.__caminos, 2, 0)
        self.moverFicha(self.__casas, 2, 1, self.__caminos, 2, 1)
        self.moverFicha(self.__casas, 1, 1, self.__caminos, 3, 0)
        self.moverFicha(self.__casas, 3, 1, self.__caminos, 3, 1)
        self.moverFicha(self.__casas, 0, 2, self.__caminos, 4, 0)
        self.moverFicha(self.__casas, 2, 2, self.__caminos, 4, 1)
        self.moverFicha(self.__casas, 1, 2, self.__caminos, 5, 0)
        self.moverFicha(self.__casas, 3, 2, self.__caminos, 5, 1)
        # self.moverFicha(self.__casas, 0, 3, self.__caminos, 0, 0)
        # self.moverFicha(self.__casas, 2, 3, self.__caminos, 0, 1)
        # self.moverFicha(self.__casas, 1, 3, self.__caminos, 1, 0)
        # self.moverFicha(self.__casas, 3, 3, self.__caminos, 1, 1)
        self.relocateAll()

    def moverFicha(self, desde, iD, jD, hasta, iH, jH):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True
        

app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
application = Ventana()
application.show()
sys.exit(app.exec())
