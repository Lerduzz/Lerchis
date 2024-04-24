import sys, time, random, qdarkstyle
from PyQt5.QtCore import QObject, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem, QMenu, QAction
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


class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego() 
        self.ui.setupUi(self)
        self.ui.btnTirar.clicked.connect(self.tirarDados)
        self.ui.dado1.clicked.connect(self.tirarDados)
        self.ui.dado2.clicked.connect(self.tirarDados)
        self.ui.btnNuevaPartida.clicked.connect(self.nuevaPartida)
        self.ui.btnTerminarPartida.clicked.connect(self.terminarPartida)
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.__cuentaDoble = 0
        self.__jugando = False
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
        self.__icons = [QIcon(),QIcon(),QIcon(),QIcon()]
        self.__icons[0].addPixmap(QPixmap(":/fichas/ficha0.png"), QIcon.Normal, QIcon.Off)
        self.__icons[1].addPixmap(QPixmap(":/fichas/ficha1.png"), QIcon.Normal, QIcon.Off)
        self.__icons[2].addPixmap(QPixmap(":/fichas/ficha2.png"), QIcon.Normal, QIcon.Off)
        self.__icons[3].addPixmap(QPixmap(":/fichas/ficha3.png"), QIcon.Normal, QIcon.Off)
        self.__names = ['Jugador rojo','Jugador verde','Jugador azul','Jugador naranja']
        self.__dadosTirados = False
        self.__disponibleDado1 = False
        self.__disponibleDado2 = False
        self.__disponibleBonusMatar = False
        self.__disponibleBonusLlegar = False
        
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.resizeAll()
        self.relocateAll()

    def abrirMenu(self, sender):
        menu = QMenu(self)
        count = 0

        iconD1 = QIcon()
        iconD1.addPixmap(QPixmap(f":/dados/dado{self.__turno}{self.__dado1}.png"), QIcon.Normal, QIcon.Off)
        actionD1 = QAction(iconD1, 'Primer dado')
        if self.__disponibleDado1:
            if self.estaEnCasa(sender):
                if self.__dado1 == 5 and self.puedeSalir():
                    menu.addAction(actionD1)
                    count += 1
            else:
                if self.puedeMover(sender, self.__dado1):
                    menu.addAction(actionD1)
                    count += 1
        
        iconD2 = QIcon()
        iconD2.addPixmap(QPixmap(f":/dados/dado{self.__turno}{self.__dado2}.png"), QIcon.Normal, QIcon.Off)
        actionD2 = QAction(iconD2, 'Segundo dado')
        if self.__disponibleDado2:
            if self.estaEnCasa(sender):
                if self.__dado2 == 5 and self.puedeSalir():
                    menu.addAction(actionD2)
                    count += 1
            else:
                if self.puedeMover(sender, self.__dado2):
                    menu.addAction(actionD2)
                    count += 1

        iconD12 = QIcon()
        iconD12.addPixmap(QPixmap(f":/dados/dado{self.__turno}s{self.__dado1 + self.__dado2}.png"), QIcon.Normal, QIcon.Off)
        actionD12 = QAction(iconD12, 'Ambos dados')
        if self.__disponibleDado1 and self.__disponibleDado2:
            if not self.estaEnCasa(sender):
                if self.puedeMover(sender, self.__dado1 + self.__dado2):
                    menu.addAction(actionD12)
                    count += 1
        
        if count > 0:
            pos = QPoint(sender.x() + sender.width(), sender.y())
            actionR = menu.exec_(self.mapToGlobal(pos))
            if actionR == actionD1:
                return 1
            elif actionR == actionD2:
                return 2
            elif actionR == actionD12:
                return 3
        return 0
        

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
        self.__dadosTirados = True
        self.__disponibleDado1 = True
        self.__disponibleDado2 = True
        self.ui.listHistorial.addItem(QListWidgetItem(self.__icons[self.__turno], f'{self.__names[self.__turno]} tira los dados y saca {s1}:{s2}.'))
        self.ui.listHistorial.setCurrentRow(self.ui.listHistorial.count() - 1)
        if not self.puedeJugar() or (self.__dado1 == self.__dado2 and self.__cuentaDoble >= 2):
            if s1 != s2:
                self.showWarning('Sin movimientos', 'Has perdido el turno porque no tienes movimientos.\n\nSugerencias:\n- Para sacar una ficha necesitas un 5 en un dado.')
            else:
                if self.__cuentaDoble >= 2:
                    self.showCritical('Mala suerte', 'Has sacado pareja 3 veces seguidas.\nTu ficha más adelantada será devuelta a casa.')
                else:
                    self.showWarning('Sin movimientos', 'No tienes movimientos disponibles.\nPuedes volver a tirar los dados porque te cayó una pareja.\n\nSugerencias:\n- Para sacar una ficha necesitas un 5 en un dado.')
            self.cambioDeTurno()

    def puedeJugar(self):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            ficha = self.__fichas[i]
            if self.estaEnCasa(ficha):
                if (self.__disponibleDado1 and self.__dado1 == 5) or (self.__disponibleDado2 and self.__dado2 == 5):
                    if self.puedeSalir():
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
        menuResp = self.abrirMenu(self.sender())
        mover = True
        if self.estaEnCasa(self.sender()):
            salio = False
            if self.__disponibleDado1 and menuResp == 1 and self.__dado1 == 5:
                if self.salirDeCasa(self.sender()):
                    self.__disponibleDado1 = False
                    salio = True
            if not salio and self.__disponibleDado2 and menuResp == 2 and self.__dado2 == 5:
                if self.salirDeCasa(self.sender()):
                    self.__disponibleDado2 = False
                    salio = True
            if not salio:
                mover = False
        if mover:
            movio = False
            total = 0
            usadoDado1 = False
            usadoDado2 = False
            usadoBonus1 = False
            usadoBonus2 = False
            if self.__disponibleDado1 and (menuResp == 1 or menuResp == 3):
                total += self.__dado1
                usadoDado1 = True
            if self.__disponibleDado2 and (menuResp == 2 or menuResp == 3):
                total += self.__dado2
                usadoDado2 = True
            if self.__disponibleBonusLlegar:
                total += 10
                usadoBonus1 = True
            if self.__disponibleBonusMatar:
                total += 20
                usadoBonus2 = True
            if total > 0:
                posI, posJ = self.obtenerPosRuta(self.sender())
                if posI + total < len(self.__rutas[self.__turno]):
                    for j in range(len(self.__rutas[self.__turno][posI + total])):
                        if self.__rutas[self.__turno][posI + total][j] == None and not self.hayPuenteEnMedio(posI, posI + total):
                            if self.moverFicha(self.__rutas[self.__turno], posI, posJ, self.__rutas[self.__turno], posI + total, j):
                                self.relocateAll()
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
                                if posI + total == len(self.__rutas[self.__turno]) - 1:
                                    self.__disponibleBonusLlegar = True
        if not self.puedeJugar():
            self.cambioDeTurno()

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
        repetir = False
        if self.__dado1 == self.__dado2:
            if self.__cuentaDoble < 2:
                self.__cuentaDoble += 1
                repetir = True
            else:
                self.virarMasAdelantada()
        if not repetir:
            self.__cuentaDoble = 0
            self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
        self.mostrarDados(0, 0)
        self.ui.btnTirar.setEnabled(True)
        self.__dadosTirados = False

    def virarMasAdelantada(self):
        for i in range(len(self.__rutas[self.__turno]) - 2, -1, -1):
            for j in range(len(self.__rutas[self.__turno][i])):
                ficha = self.__rutas[self.__turno][i][j]
                if ficha != None and self.esMia(ficha):
                    self.matarFicha(ficha)
                    return True
        return False
        
    def nuevaPartida(self):
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.__cuentaDoble = 0
        self.__jugando = True
        self.ui.btnTirar.setEnabled(True)
        self.ui.btnNuevaPartida.setEnabled(False)
        self.ui.checkPlayer0.setEnabled(False)
        self.ui.checkPlayer1.setEnabled(False)
        self.ui.checkPlayer2.setEnabled(False)
        self.ui.checkPlayer3.setEnabled(False)
        self.ui.txtNamePlayer0.setEnabled(False)
        self.ui.txtNamePlayer1.setEnabled(False)
        self.ui.txtNamePlayer2.setEnabled(False)
        self.ui.txtNamePlayer3.setEnabled(False)
        self.ui.btnTerminarPartida.setEnabled(True)

    def terminarPartida(self):        
        self.ui.btnTerminarPartida.setEnabled(False)
        self.ui.btnTirar.setEnabled(False)
        self.ui.btnNuevaPartida.setEnabled(True)
        self.ui.checkPlayer0.setEnabled(True)
        self.ui.checkPlayer1.setEnabled(True)
        self.ui.checkPlayer2.setEnabled(True)
        self.ui.checkPlayer3.setEnabled(True)
        self.ui.txtNamePlayer0.setEnabled(True)
        self.ui.txtNamePlayer1.setEnabled(True)
        self.ui.txtNamePlayer2.setEnabled(True)
        self.ui.txtNamePlayer3.setEnabled(True)

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


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
application = Ventana()
application.show()
sys.exit(app.exec())

# TODO: El bonus de matar no se puede caminar con la misma ficha.
# TODO: **(La ficha que mata no puede volver a ser movida a menos que otra camine su bonus)**
# TODO: **(Animar el movimiento de las fichas por el tablero)**
# TODO: Detectar victoria.
# TODO: Saltarse el turno del que termina (En caso de que se quiera continuar la partida luego de que gane uno).
# TODO: Si te queda una sola ficha y a esta le queda 6 movimientos o menos para entrar tiras con un solo dado.
# TODO: *Implementar la IA.
# TODO: *Implementar modo online.
# TODO: Mejorar la interfaz de nueva partida para que se pueda elegir de manera individual si un jugador va a ser LOCAL, ONLINE, IA, INACTIVO.
# TODO: La funcion de nueva partida deve devolver las fichas al inicio.
