import sys, time, random, qdarkstyle
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
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


# class TesterWorker(QObject):
#     finished = pyqtSignal()
#     progress = pyqtSignal(int)
# 
#     def __init__(self, start, limit):
#         super().__init__()
#         self.__start = start
#         self.__limit = limit
# 
#     def run(self):
#         while self.__start < self.__limit:
#             self.progress.emit(self.__start)
#             self.__start += 1
#             time.sleep(0.25)
#         self.finished.emit()


class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego() 
        self.ui.setupUi(self)
        self.ui.btnTirar.clicked.connect(self.tirarDados)
        self.ui.btnNuevaPartida.clicked.connect(self.nuevaPartida)
        self.__dado1 = 6
        self.__dado2 = 6
        self.__turno = 0
        self.__jugando = False
        self.__fichas = [self.ui.ficha00,self.ui.ficha01,self.ui.ficha02,self.ui.ficha03,self.ui.ficha10,self.ui.ficha11,self.ui.ficha12,self.ui.ficha13,self.ui.ficha20,self.ui.ficha21,self.ui.ficha22,self.ui.ficha23,self.ui.ficha30,self.ui.ficha31,self.ui.ficha32,self.ui.ficha33]
        for f in self.__fichas:
            f.clicked.connect(self.jugarFicha)
        self.__casas = [[self.ui.ficha00,self.ui.ficha01,self.ui.ficha02,self.ui.ficha03],[self.ui.ficha10,self.ui.ficha11,self.ui.ficha12,self.ui.ficha13],[self.ui.ficha20,self.ui.ficha21,self.ui.ficha22,self.ui.ficha23],[self.ui.ficha30,self.ui.ficha31,self.ui.ficha32,self.ui.ficha33]]
        self.__caminos = [[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]
        self.__posCaminos = [(250,0,0),(250,50,0),(250,100,0),(250,150,0),(250,200,0),(250,250,2),(250,250,3),(250,250,4),(200,250,1),(150,250,1),(100,250,1),(50,250,1),(0,250,1),(0,400,1),(0,550,1),(50,550,1),(100,550,1),(150,550,1),(200,550,1),(250,700,5),(250,700,6),(250,700,7),(250,700,0),(250,750,0),(250,800,0),(250,850,0),(250,900,0),(400,900,0),(550,900,0),(550,850,0),(550,800,0),(550,750,0),(550,700,0),(700,700,8),(700,700,9),(700,700,10),(700,550,1),(750,550,1),(800,550,1),(850,550,1),(900,550,1),(900,400,1),(900,250,1),(850,250,1),(800,250,1),(750,250,1),(700,250,1),(700,250,11),(700,250,12),(700,250,13),(550,200,0),(550,150,0),(550,100,0),(550,50,0),(550,0,0),(400,0,0)]
        self.__rutas = [[],[],[],[]]
        for i in range(3, 56):
            self.__rutas[0].append(self.__caminos[i])
        for i in range(17, 56):
            self.__rutas[1].append(self.__caminos[i])
        for i in range(0, 14):
            self.__rutas[1].append(self.__caminos[i])
        for i in range(31, 56):
            self.__rutas[2].append(self.__caminos[i])        
        for i in range(0, 28):
            self.__rutas[2].append(self.__caminos[i])        
        for i in range(45, 56):
            self.__rutas[3].append(self.__caminos[i])
        for i in range(0, 42):
            self.__rutas[3].append(self.__caminos[i])        

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
            if i < len(self.__posCaminos):
                x, y, o = self.__posCaminos[i]
                for j in range(2):
                    if self.__caminos[i][j] != None:
                        xR, yR = self.calcularPosicionCasilla(x, y, o, j, h, hCasilla, hFicha)
                        self.__caminos[i][j].move(xR, yR)

    def calcularPosicionCasilla(self, x, y, o, i, h, hC, hF):
        dX = x * h // 950
        dY = y * h // 950
        xR, yR = (dX, dY)
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
        elif o == 3:
            xR = dX + hF if i == 0 else dX + hF * 2 - hF // 3
            yR = dY + hF if i == 0 else dY + hF * 2 - hF // 3
        elif o == 4:
            xR = dX if i == 0 else dX + hF // 2
            yR = dY + hC // 2 - hF // 4 if i == 0 else dY + hC // 2 + hF // 2 + hF // 10        
        elif o == 5:
            xR = dX if i == 0 else dX + hF // 2
            yR = dY - hF - hC // 2 + hF // 4 if i == 0 else dY - hF - hC // 2 - hF // 2 - hF // 10
        elif o == 6:
            xR = dX + hF if i == 0 else dX + hF * 2 - hF // 3
            yR = dY - hF * 2 if i == 0 else dY - hF * 3 + hF // 3
        elif o == 7:
            xR = dX + hC // 2 - hF // 4 if i == 0 else dX + hC // 2 + hF // 2 + hF // 10
            yR = dY - hF if i == 0 else dY - hF - hF // 2        
        elif o == 8:
            xR = dX - hF - hC // 2 + hF // 4 if i == 0 else dX - hF - hC // 2 - hF // 2 - hF // 10
            yR = dY - hF if i == 0 else dY - hF - hF // 2
        elif o == 9:
            xR = dX - hF * 2 if i == 0 else dX - hF * 3 + hF // 3
            yR = dY - hF * 2 if i == 0 else dY - hF * 3 + hF // 3
        elif o == 10:
            xR = dX - hF if i == 0 else dX - hF - hF // 2
            yR = dY - hF - hC // 2 + hF // 4 if i == 0 else dY - hF - hC // 2 - hF // 2 - hF // 10
        elif o == 11:
            xR = dX - hF if i == 0 else dX - hF - hF // 2
            yR = dY + hC // 2 - hF // 4 if i == 0 else dY + hC // 2 + hF // 2 + hF // 10
        elif o == 12:
            xR = dX - hF * 2 if i == 0 else dX - hF * 3 + hF // 3
            yR = dY + hF if i == 0 else dY + hF * 2 - hF // 3
        elif o == 13:
            xR = dX - hF - hC // 2 + hF // 4 if i == 0 else dX - hF - hC // 2 - hF // 2 - hF // 10
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
        self.ui.checkDado1.setText(f'Dado # 1 => {s1}.')
        self.ui.checkDado2.setText(f'Dado # 2 => {s2}.')
        self.ui.checkDado1.setEnabled(True)
        self.ui.checkDado2.setEnabled(True)
        if not self.puedeJugar():
            self.cambioDeTurno()

    def puedeJugar(self):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            ficha = self.__fichas[i]
            if self.estaEnCasa(ficha):
                if (self.ui.checkDado1.isEnabled() and self.__dado1 == 5) or (self.ui.checkDado2.isEnabled() and self.__dado2 == 5):
                    # TODO: Comprobar que no este bloqueada la salida.
                    return True
            else:
                dist = self.cuantoCamina(ficha)
                if (self.ui.checkDado1.isEnabled() and self.__dado1 <= dist) or (self.ui.checkDado2.isEnabled() and self.__dado2 <= dist):
                    # TODO: Verificar los bonus.
                    return True
        return False

    def estaEnCasa(self, ficha):
        for fC in self.__casas[self.__turno]:
            if fC != None and ficha != None and fC == ficha:
                return True
        return False

    def cuantoCamina(self, ficha):
        if self.estaEnCasa(ficha):
            return 0
        startPos = 0
        checkPos = 0
        for casilla in self.__rutas[self.__turno]:
            if casilla[0] == ficha or casilla[1] == ficha:
                startPos = checkPos
                break
            checkPos += 1
        return len(self.__rutas[self.__turno]) - startPos - 1

    def esMia(self, ficha):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            if ficha == self.__fichas[i]:
                return True
        return False

    def jugarFicha(self):
        if self.esMia(self.sender()):
            print(f'La ficha camina: {self.cuantoCamina(self.sender())}.')
            mover = True
            # Manejar la salida de casa.
            if self.estaEnCasa(self.sender()):
                salio = False
                # Verificar salida ocupada.
                s1 = self.__rutas[self.__turno][0][0]
                s2 = self.__rutas[self.__turno][0][1]
                if s1 == None or s2 == None or not self.esMia(s1) or not self.esMia(s2):
                    # Verificar dado 1.
                    if self.ui.checkDado1.isChecked():
                        if self.__dado1 == 5:
                            self.salirDeCasa(self.sender())
                            self.ui.checkDado1.setChecked(False)
                            self.ui.checkDado1.setEnabled(False)
                            salio = True
                    # Verificar dado 2.
                    if not salio and self.ui.checkDado2.isChecked():
                        if self.__dado2 == 5:
                            self.salirDeCasa(self.sender())
                            self.ui.checkDado2.setChecked(False)
                            self.ui.checkDado2.setEnabled(False)
                            salio = True
                if not salio:
                    mover = False
            # Manejar la caminadera por el tablero.
            # else:
            if mover:
                dist = self.cuantoCamina(self.sender())
                total = 0
                if self.ui.checkDado1.isChecked():
                    total += self.__dado1
                if self.ui.checkDado2.isChecked():
                    total += self.__dado2
                # TODO: Sumar bonus seleccionados.
                if total > 0 and total <= dist:
                    # TODO: la ficha se encuentra en la ruta... 
                    # hay que encontrar su posicion... 
                    # encontrar espacio en la posicion de destino.
                    posI = 0
                    posJ = 0
                    for i in range(len(self.__rutas[self.__turno])):
                        if self.__rutas[self.__turno][i][0] == self.sender():
                            posI = i
                            posJ = 0
                        if self.__rutas[self.__turno][i][1] == self.sender():
                            posI = i
                            posJ = 1
                    dest = self.__rutas[self.__turno][posI + total]
                    s1 = self.__rutas[self.__turno][posI + total][0]
                    s2 = self.__rutas[self.__turno][posI + total][1]
                    if s1 == None:
                        if self.moverFicha(self.__rutas[self.__turno], posI, posJ, self.__rutas[self.__turno], posI + total, 0):
                            self.relocateAll()
                            if self.ui.checkDado1.isChecked():
                                self.ui.checkDado1.setChecked(False)
                                self.ui.checkDado1.setEnabled(False)
                            if self.ui.checkDado2.isChecked():
                                self.ui.checkDado2.setChecked(False)
                                self.ui.checkDado2.setEnabled(False)
                    elif s2 == None:
                        if self.moverFicha(self.__rutas[self.__turno], posI, posJ, self.__rutas[self.__turno], posI + total, 1):
                            self.relocateAll()
                            if self.ui.checkDado1.isChecked():
                                self.ui.checkDado1.setChecked(False)
                                self.ui.checkDado1.setEnabled(False)
                            if self.ui.checkDado2.isChecked():
                                self.ui.checkDado2.setChecked(False)
                                self.ui.checkDado2.setEnabled(False)
        else:
            print('¡La ficha no es mia!')
        if not self.puedeJugar():
            self.cambioDeTurno()

    def salirDeCasa(self, ficha):
        pos = 0
        for i in range(4):
            if ficha == self.__casas[self.__turno][i]:
                pos = i
                break
        if self.__rutas[self.__turno][0][0] == None:
            if self.moverFicha(self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 0):
                self.relocateAll()
        elif self.__rutas[self.__turno][0][1] == None:
            if self.moverFicha(self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 1):
                self.relocateAll()

    def cambioDeTurno(self):
        self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
        self.mostrarDados(self.__dado1, self.__dado2)
        self.prepararDados()
        
    def prepararDados(self):
        self.ui.btnTirar.setEnabled(True)
        self.ui.checkDado1.setEnabled(False)
        self.ui.checkDado2.setEnabled(False)
        self.ui.checkMeta.setEnabled(False)
        self.ui.checkMata.setEnabled(False)
        self.ui.checkDado1.setChecked(False)
        self.ui.checkDado2.setChecked(False)
        self.ui.checkMeta.setChecked(False)
        self.ui.checkMata.setChecked(False)

    def nuevaPartida(self):
        self.__dado1 = 6
        self.__dado2 = 6
        self.__turno = 0
        self.__jugando = True
        self.prepararDados()
        self.showInfo('Nueva partida', 'Ha comenzado una nueva partida, el color de los dados indica a que jugador le toca el turno.\n\nSugerencias:\n- Al inicio de cada turno hay que tirar los dados.')

    def moverFicha(self, desde, iD, jD, hasta, iH, jH):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True

    def showCritical(self, title, text):
        QMessageBox.critical(self, title, text)

    def showWarning(self, title, text):
        QMessageBox.warning(self, title, text)

    def showInfo(self, title, text):
        QMessageBox.information(self, title, text)

    # def runTester(self):
    #     self.ui.btnNuevaPartida.setEnabled(False)
    #     if (not self.moverFicha(self.__casas, 0, 3, self.__caminos, 0, 0)):
    #         self.moverFicha(self.__caminos, len(self.__posCaminos) - 1, 0, self.__caminos, 0, 0)
    #     if (not self.moverFicha(self.__casas, 2, 3, self.__caminos, 0, 1)):
    #         self.moverFicha(self.__caminos, len(self.__posCaminos) - 1, 1, self.__caminos, 0, 1) 
    #     self.relocateAll()
    #     self.__testerThread = QThread()
    #     self.__testerWorker = TesterWorker(0, len(self.__posCaminos))
    #     self.__testerWorker.moveToThread(self.__testerThread)
    #     self.__testerThread.started.connect(self.__testerWorker.run)
    #     self.__testerWorker.finished.connect(self.__testerThread.quit)
    #     self.__testerWorker.finished.connect(self.__testerWorker.deleteLater)
    #     self.__testerThread.finished.connect(self.__testerThread.deleteLater)
    #     self.__testerWorker.progress.connect(self.progressTest)
    #     self.__testerWorker.finished.connect(self.finishTest)        
    #     self.__testerThread.start()

    # def progressTest(self, value):
    #     self.moverFicha(self.__caminos, value - 1, 0, self.__caminos, value, 0)
    #     self.moverFicha(self.__caminos, value - 1, 1, self.__caminos, value, 1)
    #     self.relocateAll()

    # def finishTest(self):
    #     self.ui.btnNuevaPartida.setEnabled(True)


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
application = Ventana()
application.show()
sys.exit(app.exec())
