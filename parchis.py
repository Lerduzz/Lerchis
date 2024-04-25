import sys, time, random, qdarkstyle
from PyQt5.QtCore import QObject, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMenu, QAction
from parchis_ui import Ui_VentanaJuego

class DadosWorker(QObject):
    finished = pyqtSignal(int, int)
    progress = pyqtSignal(int, int)

    def __init__(self, s1, s2):
        super().__init__()
        self.__s1 = s1
        self.__s2 = s2
        self.__r1 = random.randint(1, 6)
        self.__r2 = random.randint(1, 6)

    def run(self):
        d1C = 0
        d2C = 0
        alt = random.randint(1, 6)
        flag = 0
        skip = random.randint(1, 2)
        m1 = random.randint(2, 4)
        m2 = random.randint(2, 4)
        while d1C < m1 or d2C < m2:
            if alt <= 3:
                if flag >= skip:
                    d1C += 1 if d1C < m1 and self.__s1 == self.__r1 else 0
                    self.__s1 += 1 if d1C < m1 else 0
                    self.__s1 = 1 if self.__s1 > 6 else self.__s1
                    flag = 0
                else:
                    flag += 1
            else:
                d1C += 1 if d1C < m1 and self.__s1 == self.__r1 else 0
                self.__s1 += 1 if d1C < m1 else 0
                self.__s1 = 1 if self.__s1 > 6 else self.__s1
            if alt >= 4:
                if flag >= skip:
                    d2C += 1 if d2C < m2 and self.__s2 == self.__r2 else 0
                    self.__s2 += 1 if d2C < m2 else 0
                    self.__s2 = 1 if self.__s2 > 6 else self.__s2
                    flag = 0
                else:
                    flag += 1
            else:
                d2C += 1 if d2C < m2 and self.__s2 == self.__r2 else 0
                self.__s2 += 1 if d2C < m2 else 0
                self.__s2 = 1 if self.__s2 > 6 else self.__s2
            self.progress.emit(self.__s1, self.__s2)
            time.sleep(0.01)
        self.finished.emit(self.__r1, self.__r2)


class TurnoWorker(QObject):
    started = pyqtSignal(int)
    finished = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, start):
        super().__init__()
        self.__max = start
        self.__value = 0
        self.__interval = 0.9

    def run(self):
        self.started.emit(self.__max)
        while self.__value < self.__max:
            self.progress.emit(self.__value)
            self.__value += 1
            time.sleep(self.__interval)
        self.finished.emit(self.__value)

    def faster(self):
        self.__interval = 0.025


class ReactivarWorker(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        count = 0
        while count < 5:
            time.sleep(0.25)
            count += 1
        self.finished.emit()


class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego()
        self.ui.setupUi(self)
        self.ui.dado1.clicked.connect(self.tirarDados)
        self.ui.dado2.clicked.connect(self.tirarDados)
        self.ui.btnNuevaPartida.clicked.connect(self.nuevaPartida)
        self.ui.btnTerminarPartida.clicked.connect(self.terminarPartida)
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__fichas = [self.ui.ficha00,self.ui.ficha01,self.ui.ficha02,self.ui.ficha03,self.ui.ficha10,self.ui.ficha11,self.ui.ficha12,self.ui.ficha13,self.ui.ficha20,self.ui.ficha21,self.ui.ficha22,self.ui.ficha23,self.ui.ficha30,self.ui.ficha31,self.ui.ficha32,self.ui.ficha33]
        for f in self.__fichas:
            f.clicked.connect(self.jugarFicha)
        self.__casas = [[self.ui.ficha00,self.ui.ficha01,self.ui.ficha02,self.ui.ficha03],[self.ui.ficha10,self.ui.ficha11,self.ui.ficha12,self.ui.ficha13],[self.ui.ficha20,self.ui.ficha21,self.ui.ficha22,self.ui.ficha23],[self.ui.ficha30,self.ui.ficha31,self.ui.ficha32,self.ui.ficha33]]
        self.__caminos = [[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None]]
        self.__posCaminos = [(250,0,0),(250,50,0),(250,100,0),(250,150,0),(250,200,0),(250,250,2),(250,250,3),(250,250,4),(200,250,1),(150,250,1),(100,250,1),(50,250,1),(0,250,1),(0,400,1),(0,550,1),(50,550,1),(100,550,1),(150,550,1),(200,550,1),(250,700,5),(250,700,6),(250,700,7),(250,700,0),(250,750,0),(250,800,0),(250,850,0),(250,900,0),(400,900,0),(550,900,0),(550,850,0),(550,800,0),(550,750,0),(550,700,0),(700,700,8),(700,700,9),(700,700,10),(700,550,1),(750,550,1),(800,550,1),(850,550,1),(900,550,1),(900,400,1),(900,250,1),(850,250,1),(800,250,1),(750,250,1),(700,250,1),(700,250,11),(700,250,12),(700,250,13),(550,200,0),(550,150,0),(550,100,0),(550,50,0),(550,0,0),(400,0,0)]
        self.__metas = [[[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None,None,None]],[[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None,None,None]],[[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None,None,None]],[[None,None],[None,None],[None,None],[None,None],[None,None],[None,None],[None,None,None,None]]]
        self.__posMetas = [[(400,50,0),(400,100,0),(400,150,0),(400,200,0),(400,250,0),(400,300,0),(475,400,14)],[(50,400,1),(100,400,1),(150,400,1),(200,400,1),(250,400,1),(300,400,1),(400,475,15)],[(400,850,0),(400,800,0),(400,750,0),(400,700,0),(400,650,0),(400,600,0),(475,550,16)],[(850,400,1),(800,400,1),(750,400,1),(700,400,1),(650,400,1),(600,400,1),(550,475,17)]]
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
        for i in range(4):
            self.__rutas[i] += self.__metas[i]
        self.__excluir = [0, 6, 10, 14, 20, 24, 28, 34, 38, 42, 48, 52, 53, 54, 55, 56, 57, 58, 59]
        self.__bridges = [0, 14, 28, 42]
        self.__names = ['ROJO','VERDE','AZUL','NARANJA']
        self.__icons = [QIcon(),QIcon(),QIcon(),QIcon()]
        self.__icons[0].addPixmap(QPixmap(":/fichas/ficha0.png"), QIcon.Normal, QIcon.Off)
        self.__icons[1].addPixmap(QPixmap(":/fichas/ficha1.png"), QIcon.Normal, QIcon.Off)
        self.__icons[2].addPixmap(QPixmap(":/fichas/ficha2.png"), QIcon.Normal, QIcon.Off)
        self.__icons[3].addPixmap(QPixmap(":/fichas/ficha3.png"), QIcon.Normal, QIcon.Off)
        self.__jugando = False
        self.__dadosTirados = False
        self.__disponibleDado1 = False
        self.__disponibleDado2 = False
        self.__disponibleBonusMatar = False
        self.__disponibleBonusLlegar = False
        self.__contandoTurno = False
        
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.resizeAll()
        self.relocateAll()

    def abrirMenu(self, sender):
        menu = QMenu(self)
        count = 0
        iconDado1 = QIcon()
        iconDado1.addPixmap(QPixmap(f":/dados/dado{self.__turno}{self.__dado1}.png"), QIcon.Normal, QIcon.Off)
        actionDado1 = QAction(iconDado1, 'Primer dado')
        iconDado2 = QIcon()
        iconDado2.addPixmap(QPixmap(f":/dados/dado{self.__turno}{self.__dado2}.png"), QIcon.Normal, QIcon.Off)
        actionDado2 = QAction(iconDado2, 'Segundo dado')
        iconBonus1 = QIcon()
        iconBonus1.addPixmap(QPixmap(f":/dados/dado{self.__turno}s10.png"), QIcon.Normal, QIcon.Off)
        actionBonus1 = QAction(iconBonus1, 'Bono por llegar')
        iconBonus2 = QIcon()
        iconBonus2.addPixmap(QPixmap(f":/dados/dado{self.__turno}s20.png"), QIcon.Normal, QIcon.Off)
        actionBonus2 = QAction(iconBonus2, 'Bono por matar')
        iconDado1Dado2 = QIcon()
        iconDado1Dado2.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado1 + self.__dado2}.png"), QIcon.Normal, QIcon.Off)
        actionDado1Dado2 = QAction(iconDado1Dado2, 'Todos los dados')
        iconDado1Bonus1 = QIcon()
        iconDado1Bonus1.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado1 + 10}.png"), QIcon.Normal, QIcon.Off)
        actionDado1Bonus1 = QAction(iconDado1Bonus1, 'Primer dado + Bono por llegar')
        iconDado1Bonus2 = QIcon()
        iconDado1Bonus2.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado1 + 20}.png"), QIcon.Normal, QIcon.Off)
        actionDado1Bonus2 = QAction(iconDado1Bonus2, 'Primer dado + Bono por matar')
        iconDado2Bonus1 = QIcon()
        iconDado2Bonus1.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado2 + 10}.png"), QIcon.Normal, QIcon.Off)
        actionDado2Bonus1 = QAction(iconDado2Bonus1, 'Segundo dado + Bono por llegar')
        iconDado2Bonus2 = QIcon()
        iconDado2Bonus2.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado2 + 20}.png"), QIcon.Normal, QIcon.Off)
        actionDado2Bonus2 = QAction(iconDado2Bonus2, 'Segundo dado + Bono por matar')
        iconBonus1Bonus2 = QIcon()
        iconBonus1Bonus2.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{30}.png"), QIcon.Normal, QIcon.Off)
        actionBonus1Bonus2 = QAction(iconBonus1Bonus2, 'Todos los bonos')
        if self.__disponibleDado1:
            if self.estaEnCasa(sender):
                if self.__dado1 == 5 and self.puedeSalir():
                    menu.addAction(actionDado1)
                    count += 1
            else:
                if self.puedeMover(sender, self.__dado1):
                    menu.addAction(actionDado1)
                    count += 1        
        if self.__disponibleDado2:
            if self.estaEnCasa(sender):
                if self.__dado2 == 5 and self.puedeSalir():
                    menu.addAction(actionDado2)
                    count += 1
            else:
                if self.puedeMover(sender, self.__dado2):
                    menu.addAction(actionDado2)
                    count += 1
        if self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender) and self.puedeMover(sender, 10):
                menu.addAction(actionBonus1)
                count += 1
        if self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender) and self.puedeMover(sender, 20):
                menu.addAction(actionBonus2)
                count += 1
        if self.__disponibleDado1 and self.__disponibleDado2:
            if self.estaEnCasa(sender):
                if self.__dado1 + self.__dado2 == 5 and self.puedeSalir():
                    menu.addAction(actionDado1Dado2)
                    count += 1
            else:
                if self.puedeMover(sender, self.__dado1 + self.__dado2):
                    menu.addAction(actionDado1Dado2)
                    count += 1
        if self.__disponibleDado1 and self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado1 + 10):
                    menu.addAction(actionDado1Bonus1)
                    count += 1
        if self.__disponibleDado1 and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado1 + 20):
                    menu.addAction(actionDado1Bonus2)
                    count += 1
        if self.__disponibleDado2 and self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado2 + 10):
                    menu.addAction(actionDado2Bonus1)
                    count += 1
        if self.__disponibleDado2 and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado2 + 20):
                    menu.addAction(actionDado2Bonus2)
                    count += 1
        if self.__disponibleBonusLlegar and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, 30):
                    menu.addAction(actionBonus1Bonus2)
                    count += 1
        if count > 0:
            pos = QPoint(sender.x() + sender.width(), sender.y())
            actionR = menu.exec_(self.mapToGlobal(pos))
            if actionR == actionDado1:
                return [1]
            elif actionR == actionDado2:
                return [2]
            elif actionR == actionBonus1:
                return [3]
            elif actionR == actionBonus2:
                return [4]
            elif actionR == actionDado1Dado2:
                return [1, 2]
            elif actionR == actionDado1Bonus1:
                return [1, 3]
            elif actionR == actionDado1Bonus2:
                return [1, 4]
            elif actionR == actionDado2Bonus1:
                return [2, 3]
            elif actionR == actionDado2Bonus2:
                return [2, 4]
            elif actionR == actionBonus1Bonus2:
                return [3, 4]
        return []

    def detectarJugadaAutomatica(self, sender):
        jugadasValidas = []
        if self.__disponibleDado1:
            if self.estaEnCasa(sender):
                if self.__dado1 == 5 and self.puedeSalir():
                    jugadasValidas.append([1])
            else:
                if self.puedeMover(sender, self.__dado1):
                    jugadasValidas.append([1])     
        if self.__disponibleDado2:
            if self.estaEnCasa(sender):
                if self.__dado2 == 5 and self.puedeSalir():
                    jugadasValidas.append([2])
            else:
                if self.puedeMover(sender, self.__dado2):
                    jugadasValidas.append([2])
        if self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender) and self.puedeMover(sender, 10):
                jugadasValidas.append([3])
        if self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender) and self.puedeMover(sender, 20):
                jugadasValidas.append([4])
        if self.__disponibleDado1 and self.__disponibleDado2:
            if self.estaEnCasa(sender):
                if self.__dado1 + self.__dado2 == 5 and self.puedeSalir():
                    jugadasValidas.append([1, 2])
            else:
                if self.puedeMover(sender, self.__dado1 + self.__dado2):
                    jugadasValidas.append([1, 2])
        if self.__disponibleDado1 and self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado1 + 10):
                    jugadasValidas.append([1, 3])
        if self.__disponibleDado1 and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado1 + 20):
                    jugadasValidas.append([1, 4])
        if self.__disponibleDado2 and self.__disponibleBonusLlegar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado2 + 10):
                    jugadasValidas.append([2, 3])
        if self.__disponibleDado2 and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado2 + 20):
                    jugadasValidas.append([2, 4])
        if self.__disponibleBonusLlegar and self.__disponibleBonusMatar:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, 30):
                    jugadasValidas.append([3, 4])
        return jugadasValidas[0] if len(jugadasValidas) == 1 else None

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
        for i in range(len(self.__casas)):
            casaX = (0 if i == 0 or i == 1 else 700) * h // 950
            casaY = (0 if i == 0 or i == 3 else 700) * h // 950
            for j in range(len(self.__casas[i])):
                p1 = hCasa // 2 - hFicha - hFicha // 2
                p2 = hCasa // 2 + hFicha // 2
                if self.__casas[i][j] != None:
                    self.__casas[i][j].move(casaX + (p1 if j == 0 or j == 1 else p2), casaY + (p1 if j == 0 or j == 3 else p2))
        hCasilla = 150 * h // 950
        for i in range(len(self.__caminos)):
            if i < len(self.__posCaminos):
                x, y, o = self.__posCaminos[i]
                for j in range(len(self.__caminos[i])):
                    if self.__caminos[i][j] != None:
                        xR, yR = self.calcularPosicionCasilla(x, y, o, j, h, hCasilla, hFicha)
                        self.__caminos[i][j].move(xR, yR)
        for i in range(len(self.__metas)):
            if i < len(self.__posMetas):
                for j in range(len(self.__metas[i])):
                    if j < len(self.__posMetas[i]):
                        x, y, o = self.__posMetas[i][j]
                        for k in range(len(self.__metas[i][j])):
                            if self.__metas[i][j][k] != None:
                                xR, yR = self.calcularPosicionCasilla(x, y, o, k, h, hCasilla, hFicha)
                                self.__metas[i][j][k].move(xR, yR)

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
        elif o == 14:
            xR = dX - hF if i == 0 or i == 1 else dX
            yR = dY - hF if i == 0 or i == 3 else dY
            if i == 0:
                xR -= hF * 3 // 4
            if i == 3:
                xR += hF * 3 // 4
            if i == 1 or i == 2:
                yR -= hF // 3
        elif o == 15:
            xR = dX - hF if i == 0 or i == 1 else dX
            yR = dY - hF if i == 0 or i == 3 else dY
            if i == 0:
                yR -= hF * 3 // 4
            if i == 1:
                yR += hF * 3 // 4
            if i == 2 or i == 3:
                xR -= hF // 3
        elif o == 16:
            xR = dX - hF if i == 0 or i == 1 else dX
            yR = dY - hF if i == 0 or i == 3 else dY
            if i == 1:
                xR -= hF * 3 // 4
            if i == 2:
                xR += hF * 3 // 4
            if i == 0 or i == 3:
                yR += hF // 3
        elif o == 17:
            xR = dX - hF if i == 0 or i == 1 else dX
            yR = dY - hF if i == 0 or i == 3 else dY
            if i == 3:
                yR -= hF * 3 // 4
            if i == 2:
                yR += hF * 3 // 4
            if i == 0 or i == 1:
                xR += hF // 3
        return (xR, yR)

    def tirarDados(self):
        self.ui.dado1.setEnabled(False)
        self.ui.dado2.setEnabled(False)
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
        self.insertarMensaje(f'Tira los dados y saca [{s1}]:[{s2}]')
        self.__dado1 = s1
        self.__dado2 = s2
        self.mostrarDados(s1, s2)
        self.__dadosTirados = True
        self.__disponibleDado1 = True
        self.__disponibleDado2 = True
        if s1 == s2:
            if self.__cuentaDoble < 2:
                self.__cuentaDoble += 1
                self.__repetirTirada = True
            else:
                self.virarMasAdelantada()
                if self.__contandoTurno:
                    self.__turnoWorker.faster()
                return
        else:
            self.__cuentaDoble = 0
            self.__repetirTirada = False
        if not self.puedeJugar():
            if self.__repetirTirada:
                self.iniciarReactivadorDados()
                self.insertarMensaje('Sin movimientos disponibles, vuelve a tirar los dados')
            else:
                if self.__contandoTurno:
                    self.__turnoWorker.faster()
                self.insertarMensaje('Sin movimientos disponibles, terminando turno')

    def puedeJugar(self):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            ficha = self.__fichas[i]
            if self.estaEnCasa(ficha):
                if self.puedeSalir():
                    if (self.__disponibleDado1 and self.__dado1 == 5) or (self.__disponibleDado2 and self.__dado2 == 5) or (self.__disponibleDado1 and self.__disponibleDado2 and self.__dado1 + self.__dado2 == 5):
                        return True
            else:
                mData = [(self.__disponibleDado1,self.__dado1),(self.__disponibleDado2,self.__dado2),(self.__disponibleBonusLlegar,10),(self.__disponibleBonusMatar,20)]
                for i in range(len(mData)):
                    c, v = mData[i]
                    if c:
                        if self.puedeMover(ficha, v):
                            return True
                        if i + 1 < len(mData):
                            for j in range(i + 1, len(mData)):
                                c1, v1 = mData[j]
                                if c1:
                                    v += v1
                                    if self.puedeMover(ficha, v):
                                        return True
        return False

    def puedeMover(self, ficha, pasos):
        if pasos <= 0:
            return False
        posI, posJ = self.obtenerPosRuta(ficha)
        if posI + pasos >= len(self.__rutas[self.__turno]):
            return False
        for j in range(len(self.__rutas[self.__turno][posI + pasos])):
            if self.__rutas[self.__turno][posI + pasos][j] == None and not self.hayPuenteEnMedio(posI, posI + pasos):
                return True
        return False

    def puedeSalir(self):
        s1 = self.__rutas[self.__turno][0][0]
        s2 = self.__rutas[self.__turno][0][1]
        return False if s1 != None and s2 != None and self.esMia(s1) and self.esMia(s2) else True

    def hayPuenteEnMedio(self, desde, hasta):
        for i in range(len(self.__bridges)):
            pos = self.__bridges[i]
            posOwner = self.__turno + i
            posOwner -= (4 if posOwner > 3 else 0)
            if desde >= pos:
                continue
            if hasta <= pos:
                break
            hayPuente = True
            for j in range(len(self.__rutas[self.__turno][pos])):
                if self.__rutas[self.__turno][pos][j] == None:
                    hayPuente = False
                    break
                owner, index = self.obtenerOwnerIndex(self.__rutas[self.__turno][pos][j])
                if owner != posOwner:
                    hayPuente = False
                    break
            if hayPuente:
                return True
        return False

    def obtenerPosRuta(self, ficha):
        posI = 0
        posJ = 0
        for i in range(len(self.__rutas[self.__turno])):
            for j in range(len(self.__rutas[self.__turno][i])):
                if self.__rutas[self.__turno][i][j] == ficha:
                    posI = i
                    posJ = j
                    break
        return (posI, posJ)

    def obtenerOwnerIndex(self, ficha):
        index = 0
        for i in range(len(self.__fichas)):
            if self.__fichas[i] == ficha:
                index = i
                break
        owner = 0
        while index >= 4:
            index -= 4
            owner += 1
        return (owner, index)

    def estaEnCasa(self, ficha):
        for fC in self.__casas[self.__turno]:
            if fC != None and ficha != None and fC == ficha:
                return True
        return False

    def esMia(self, ficha):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            if ficha == self.__fichas[i]:
                return True
        return False

    def jugarFicha(self):
        if not self.__jugando or not self.__dadosTirados or not self.esMia(self.sender()):
            return
        menuResp = self.detectarJugadaAutomatica(self.sender())
        if menuResp == None:
            menuResp = self.abrirMenu(self.sender())
        if len(menuResp) == 0:
            return
        if self.estaEnCasa(self.sender()):
            if self.puedeSalir():
                if self.__disponibleDado1 and 1 in menuResp and self.__dado1 == 5:
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado1 = False
                        self.insertarMensaje('Saca una ficha con el primer dado')
                elif self.__disponibleDado2 and 2 in menuResp and self.__dado2 == 5:
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado2 = False
                        self.insertarMensaje('Saca una ficha con el segundo dado')
                elif self.__disponibleDado1 and self.__disponibleDado2 and 1 in menuResp and 2 in menuResp and self.__dado1 + self.__dado2 == 5:
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado1 = False
                        self.__disponibleDado2 = False
                        self.insertarMensaje('Saca una ficha con ambos dados')
        else:
            movio = False
            total = 0
            usadoDado1 = False
            usadoDado2 = False
            usadoBonus1 = False
            usadoBonus2 = False
            if self.__disponibleDado1 and 1 in menuResp:
                total += self.__dado1
                usadoDado1 = True
            if self.__disponibleDado2 and 2 in menuResp:
                total += self.__dado2
                usadoDado2 = True
            if self.__disponibleBonusLlegar and 3 in menuResp:
                total += 10
                usadoBonus1 = True
            if self.__disponibleBonusMatar and 4 in menuResp:
                total += 20
                usadoBonus2 = True
            if total > 0:
                posI, posJ = self.obtenerPosRuta(self.sender())
                if posI + total < len(self.__rutas[self.__turno]):
                    for j in range(len(self.__rutas[self.__turno][posI + total])):
                        if self.__rutas[self.__turno][posI + total][j] == None and not self.hayPuenteEnMedio(posI, posI + total):
                            if self.moverFicha(self.__rutas[self.__turno], posI, posJ, self.__rutas[self.__turno], posI + total, j):
                                self.relocateAll()
                                mFicha = None
                                llego = False
                                if usadoDado1:
                                    self.__disponibleDado1 = False
                                if usadoDado2:
                                    self.__disponibleDado2 = False
                                if usadoBonus1:
                                    self.__disponibleBonusLlegar = False
                                if usadoBonus2:
                                    self.__disponibleBonusMatar = False
                                for jC in range(len(self.__rutas[self.__turno][posI + total])):
                                    fM = self.__rutas[self.__turno][posI + total][jC]
                                    if j != jC and fM != None and not posI + total in self.__excluir and not self.esMia(fM):
                                        if self.matarFicha(fM):
                                            self.__disponibleBonusMatar = True
                                            mFicha = fM
                                if posI + total == len(self.__rutas[self.__turno]) - 1:
                                    self.__disponibleBonusLlegar = True
                                    llego = True
                                pL = 's' if total > 1 else ''
                                if mFicha != None:
                                    oFicha, iFicha = self.obtenerOwnerIndex(mFicha)                                    
                                    self.insertarMensaje(f'Mata una ficha del jugador [{self.__names[oFicha]}] con {total} paso{pL}')
                                elif llego:
                                    self.insertarMensaje(f'Entra en la casilla de meta con {total} paso{pL}')
                                else:
                                    self.insertarMensaje(f'Camina un total de {total} paso{pL}')
        if not self.puedeJugar():
            if self.__repetirTirada:
                self.__repetirTirada = False
                self.iniciarReactivadorDados()
            else:
                if self.__contandoTurno:
                    self.__turnoWorker.faster()

    def salirDeCasa(self, ficha):
        pos = 0
        for i in range(4):
            if ficha == self.__casas[self.__turno][i]:
                pos = i
                break
        s1 = self.__rutas[self.__turno][0][0]
        s2 = self.__rutas[self.__turno][0][1]
        if s1 != None and s2 != None:
            if s1 != None and not self.esMia(s1):
                if self.matarFicha(s1):
                    self.__disponibleBonusMatar = True
            if s2 != None and not self.esMia(s2):
                if self.matarFicha(s2):
                    self.__disponibleBonusMatar = True
        s1 = self.__rutas[self.__turno][0][0]
        s2 = self.__rutas[self.__turno][0][1]
        if s1 == None:
            if self.moverFicha(self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 0):
                self.relocateAll()
                return True
        elif s2 == None:
            if self.moverFicha(self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 1):
                self.relocateAll()
                return True
        return False

    def matarFicha(self, ficha):
        posI, posJ = self.obtenerPosRuta(ficha)
        owner, index = self.obtenerOwnerIndex(ficha)
        if self.moverFicha(self.__rutas[self.__turno], posI, posJ, self.__casas, owner, index):
            self.relocateAll()
            return True
        return False

    def cambioDeTurno(self):
        if not self.__jugando:
            return
        self.insertarMensaje('>>>=====> TURNO TERMINADO <=====<<<')
        self.__cuentaDoble = 0
        self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
        estados = [self.ui.checkPlayer0.isChecked(), self.ui.checkPlayer1.isChecked(), self.ui.checkPlayer2.isChecked(), self.ui.checkPlayer3.isChecked()]
        if True in estados:
             while (not estados[self.__turno]):
                 self.__turno = 0 if self.__turno >= 3 else self.__turno + 1                
        self.prepararDados()
        self.__repetirTirada = False
        self.__tempThread = self.__turnoThread
        self.__tempWorker = self.__turnoWorker
        self.iniciarContadorTurno(30)

    def prepararDados(self):
        self.mostrarDados(0, 0)
        self.ui.dado1.setEnabled(True)
        self.ui.dado2.setEnabled(True)
        self.__dadosTirados = False
        self.__disponibleDado1 = False
        self.__disponibleDado2 = False
        self.__disponibleBonusLlegar = False
        self.__disponibleBonusMatar = False

    def virarMasAdelantada(self):
        for i in range(len(self.__rutas[self.__turno]) - 2, -1, -1):
            for j in range(len(self.__rutas[self.__turno][i])):
                ficha = self.__rutas[self.__turno][i][j]
                if ficha != None and self.esMia(ficha):
                    self.matarFicha(ficha)
                    return True
        return False
        
    def nuevaPartida(self):
        self.ui.btnNuevaPartida.setEnabled(False)
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__jugando = True
        self.__dadosTirados = False
        self.ui.dado1.setEnabled(True)
        self.ui.dado2.setEnabled(True)        
        self.ui.checkPlayer0.setEnabled(False)
        self.ui.checkPlayer1.setEnabled(False)
        self.ui.checkPlayer2.setEnabled(False)
        self.ui.checkPlayer3.setEnabled(False)
        self.ui.btnTerminarPartida.setEnabled(True)
        self.iniciarContadorTurno(30)

    def terminarPartida(self):
        self.ui.btnTerminarPartida.setEnabled(False)
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__jugando = False
        self.__dadosTirados = False
        self.ui.dado1.setEnabled(False)
        self.ui.dado2.setEnabled(False)
        self.ui.checkPlayer0.setEnabled(True)
        self.ui.checkPlayer1.setEnabled(True)
        self.ui.checkPlayer2.setEnabled(True)
        self.ui.checkPlayer3.setEnabled(True)
        self.ui.btnNuevaPartida.setEnabled(True)
        if self.__contandoTurno:
            self.__turnoWorker.faster()

    def moverFicha(self, desde, iD, jD, hasta, iH, jH):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True

    def iniciarContadorTurno(self, start):
        if not self.__contandoTurno:
            self.__contandoTurno = True
            self.__turnoThread = QThread()
            self.__turnoWorker = TurnoWorker(start)
            self.__turnoWorker.moveToThread(self.__turnoThread)
            self.__turnoThread.started.connect(self.__turnoWorker.run)
            self.__turnoWorker.finished.connect(self.__turnoThread.quit)
            self.__turnoWorker.finished.connect(self.__turnoWorker.deleteLater)
            self.__turnoThread.finished.connect(self.__turnoThread.deleteLater)
            self.__turnoWorker.started.connect(self.onContadorTurnoStarted)
            self.__turnoWorker.progress.connect(self.onContadorTurnoProgress)
            self.__turnoWorker.finished.connect(self.onContadorTurnoFinished) 
            self.__turnoThread.start()

    def onContadorTurnoStarted(self, maxValue):
        self.ui.lblTiempo.setText(str(maxValue))
        self.ui.progressTiempo.setMaximum(int(maxValue))
        self.ui.progressTiempo.setValue(0)

    def onContadorTurnoProgress(self, value):
        if value >= 0 and value <= self.ui.progressTiempo.maximum():
            self.ui.progressTiempo.setValue(value)
            self.ui.lblTiempo.setText(str(self.ui.progressTiempo.maximum() - value))

    def onContadorTurnoFinished(self, value):
        self.onContadorTurnoProgress(value)
        self.__contandoTurno = False
        self.cambioDeTurno()

    def iniciarReactivadorDados(self):
        self.__reactivarThread = QThread()
        self.__reactivarWorker = ReactivarWorker()
        self.__reactivarWorker.moveToThread(self.__reactivarThread)
        self.__reactivarThread.started.connect(self.__reactivarWorker.run)
        self.__reactivarWorker.finished.connect(self.__reactivarThread.quit)
        self.__reactivarWorker.finished.connect(self.__reactivarWorker.deleteLater)
        self.__reactivarThread.finished.connect(self.__reactivarThread.deleteLater)
        self.__reactivarWorker.finished.connect(self.prepararDados) 
        self.__reactivarThread.start()

    def insertarMensaje(self, msg):
        self.ui.listHistorial.addItem(
            QListWidgetItem(self.__icons[self.__turno], f'[{self.__names[self.__turno]}]: {msg}.')
        )
        count = self.ui.listHistorial.count()
        while count > 1024:
            self.ui.listHistorial.takeItem(0)
            count = self.ui.listHistorial.count()
        self.ui.listHistorial.setCurrentRow(count - 1)


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
application = Ventana()
application.show()
sys.exit(app.exec())

# TODO: Si solo una de tus fichas se puede mover y no hay jugada esrtategica (O sea que puede caminar todas las cantidades individuales y en ninguna come): moverla automaticamente.
# TODO: Saltarse el turno del que termina (En caso de que se quiera continuar la partida luego de que gane uno).
# TODO: Si te queda una sola ficha y a esta le queda 6 movimientos o menos para entrar tiras con un solo dado.
# TODO: La funcion de nueva partida deve devolver las fichas al inicio.
# TODO: (Informativo) Agregarle las reglas que tengo escritas en el teléfono.
# TODO: (Opcional) Animar el movimiento de las fichas por el tablero.
# TODO: (Opcional) Detectar victoria.
# TODO: (Proximamente) Implementar la IA.
# TODO: (Proximamente) Implementar modo online.
