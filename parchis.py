import os
import sys
from pygame.mixer import init as MixerInit, Sound, music as Music
import qdarkstyle
import random
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from parchis_ui import Ui_VentanaJuego
from workers.dados import DadosWorker, ReactivarWorker
from workers.turno import TurnoWorker
from utils.utils import Utils
from utils.static import InitStatic
from utils.move import MoveUtils
from ia.pro import LerchisIA


class Ventana(QMainWindow):
    messageArrived = pyqtSignal(str)

    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego()
        self.ui.setupUi(self)
        self.ui.dado1.clicked.connect(self.tirarDados)
        self.ui.dado2.clicked.connect(self.tirarDados)
        self.ui.btnNuevaPartida.clicked.connect(self.nuevaPartida)
        self.ui.btnTerminarPartida.clicked.connect(self.terminarPartida)
        self.messageArrived.connect(self.insertarMensaje)
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__fichas = InitStatic.fichas(
            self.ui, self.fichaClicEvent, self.fichaClicDerEvent
        )
        self.__posCaminos = InitStatic.posCaminos()
        self.__posMetas = InitStatic.posMetas()
        self.__excluir = InitStatic.excluir()
        self.__bridges = InitStatic.bridges()
        self.__names = InitStatic.names()
        self.__icons = InitStatic.icons()
        self.restablecerTablero()
        self.__jugando = False
        self.__dadosT = False
        self.__disponibleBono1 = False
        self.__disponibleBono2 = False
        self.__contandoTurno = False
        self.__reactivandoDados = False
        MixerInit()
        self.__sndDados = Sound(os.path.join("sounds", "dados.wav"))
        self.__sndLlegar = Sound(os.path.join("sounds", "llegar.wav"))
        self.__sndMatar = Sound(os.path.join("sounds", "matar.wav"))
        self.__sndMover = Sound(os.path.join("sounds", "mover.wav"))
        self.__sndNoMover = Sound(os.path.join("sounds", "nomover.wav"))
        self.__sndSalir = Sound(os.path.join("sounds", "salir.wav"))
        self.__sndTurno = Sound(os.path.join("sounds", "turno.wav"))
        Music.load(os.path.join("sounds", "music1.wav"))
        Music.play(-1, 0, 2500)
        self.__ia = None
        self.__iaThread = None

    def haJugado(self):
        if not self.puedeJugar():
            if self.__repetirTirada:
                self.__repetirTirada = False
                self.iniciarReactivadorDados()
            else:
                if self.__contandoTurno:
                    self.__turnoWorker.faster()

    def soyIA(self):
        ias = [
            self.ui.checkIA0.isChecked(),
            self.ui.checkIA1.isChecked(),
            self.ui.checkIA2.isChecked(),
            self.ui.checkIA3.isChecked(),
        ]
        return ias[self.__turno]

    def restablecerTablero(self):
        self.__casas = InitStatic.casas(self.ui)
        self.__caminos = InitStatic.caminos()
        self.__metas = InitStatic.metas()
        self.__rutas = InitStatic.rutas(self.__caminos, self.__metas)
        self.relocateAll()

    def resizeEvent(self, e: QResizeEvent):
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
        for i in range(len(self.__casas)):
            casaX = (0 if i == 0 or i == 1 else 700) * h // 950
            casaY = (0 if i == 0 or i == 3 else 700) * h // 950
            for j in range(len(self.__casas[i])):
                p1 = hCasa // 2 - hFicha - hFicha // 2
                p2 = hCasa // 2 + hFicha // 2
                if self.__casas[i][j] != None:
                    self.__casas[i][j].move(
                        casaX + (p1 if j == 0 or j == 1 else p2),
                        casaY + (p1 if j == 0 or j == 3 else p2),
                    )
        hCasilla = 150 * h // 950
        for i in range(len(self.__caminos)):
            if i < len(self.__posCaminos):
                x, y, o = self.__posCaminos[i]
                for j in range(len(self.__caminos[i])):
                    if self.__caminos[i][j] != None:
                        xR, yR = MoveUtils.calcularPosicionCasilla(
                            x, y, o, j, h, hCasilla, hFicha
                        )
                        self.__caminos[i][j].move(xR, yR)
        for i in range(len(self.__metas)):
            if i < len(self.__posMetas):
                for j in range(len(self.__metas[i])):
                    if j < len(self.__posMetas[i]):
                        x, y, o = self.__posMetas[i][j]
                        for k in range(len(self.__metas[i][j])):
                            if self.__metas[i][j][k] != None:
                                xR, yR = MoveUtils.calcularPosicionCasilla(
                                    x, y, o, k, h, hCasilla, hFicha
                                )
                                self.__metas[i][j][k].move(xR, yR)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif e.key() == Qt.Key.Key_Escape:
            if self.isFullScreen() or self.isMaximized():
                self.showNormal()

    def fichaClicEvent(self):
        if not Utils.puedeUsarFicha(self, self.__jugando, self.__dadosT, self.sender()):
            Sound.play(self.__sndNoMover)
            return
        self.intentaSalirDeCasa(self.sender())
        if self.estaEnCasa(self.sender()):
            return
        movs = Utils.cargarJugadasPosibles(
            self,
            self.sender(),
            self.__dado1,
            self.__dado2,
            self.__disponibleBono1,
            self.__disponibleBono2,
        )
        if len(movs) == 0:
            return
        if len(movs) == 1:
            MoveUtils.moverFichaDirecto(
                self,
                self.sender(),
                movs[0],
                self.__dado1,
                self.__dado2,
                self.__disponibleBono1,
                self.__disponibleBono2,
                self.miRuta(),
                self.__excluir,
            )
            return
        MoveUtils.moverFichaDirecto(
            self,
            self.sender(),
            MoveUtils.mayorDistancia(movs, self.__dado1, self.__dado2),
            self.__dado1,
            self.__dado2,
            self.__disponibleBono1,
            self.__disponibleBono2,
            self.miRuta(),
            self.__excluir,
        )

    def fichaClicDerEvent(self):
        if not Utils.puedeUsarFicha(self, self.__jugando, self.__dadosT, self.sender()):
            Sound.play(self.__sndNoMover)
            return
        if self.intentaSalirDeCasa(self.sender()):
            return
        mov = Utils.crearMenuContextual(
            self,
            self.sender(),
            self.__turno,
            self.__dado1,
            self.__dado2,
            self.__dado1 > 0,
            self.__dado2 > 0,
            self.__disponibleBono1,
            self.__disponibleBono2,
        )
        if len(mov) == 0:
            return
        MoveUtils.moverFichaDirecto(
            self,
            self.sender(),
            mov,
            self.__dado1,
            self.__dado2,
            self.__disponibleBono1,
            self.__disponibleBono2,
            self.miRuta(),
            self.__excluir,
        )

    def dado1Usado(self):
        self.__dado1 = 0

    def dado2Usado(self):
        self.__dado2 = 0

    def bono1Usado(self):
        self.__disponibleBono1 = False

    def bono2Usado(self):
        self.__disponibleBono2 = False

    def activarBono1(self):
        self.__disponibleBono1 = True
        Sound.play(self.__sndLlegar)

    def activarBono2(self):
        self.__disponibleBono2 = True
        Sound.play(self.__sndMatar)

    def sonidoMover(self):
        Sound.play(self.__sndMover)

    def intentaSalirDeCasa(self, ficha):
        if self.estaEnCasa(ficha):
            if self.puedeSalir():
                if self.salirDeCasa(ficha):
                    rmsg = "ambos dados"
                    if self.__dado1 == 5:
                        self.dado1Usado()
                        rmsg = "el primer dado"
                    elif self.__dado2 == 5:
                        self.dado2Usado()
                        rmsg = "el segundo dado"
                    else:
                        self.dado1Usado()
                        self.dado2Usado()
                    try:
                        self.messageArrived.emit(
                            f"Saca una ficha de su casa con {rmsg}"
                        )
                    except:
                        pass
                    return True
        return False

    def estaEnCasa(self, ficha):
        for fC in self.miCasa():
            if fC != None and ficha != None and fC == ficha:
                return True
        return False

    def puedeSalir(self):
        if self.__dado1 == 5 or self.__dado2 == 5 or self.__dado1 + self.__dado2 == 5:
            s1 = self.miRuta()[0][0]
            s2 = self.miRuta()[0][1]
            if not (s1 != None and s2 != None and self.esMia(s1) and self.esMia(s2)):
                return True
        return False

    def salirDeCasa(self, ficha):
        owner, index = self.obtenerOwnerIndex(ficha)
        if owner != self.__turno:
            return False
        mata = self.matarEnSalida()
        if MoveUtils.moverFicha(self.__casas, self.__turno, index, self.miRuta(), 0, 0):
            self.relocateAll()
            if not mata:
                Sound.play(self.__sndSalir)
            return True
        else:
            if MoveUtils.moverFicha(
                self.__casas, self.__turno, index, self.miRuta(), 0, 1
            ):
                self.relocateAll()
                if not mata:
                    Sound.play(self.__sndSalir)
                return True
        return False

    def matarEnSalida(self):
        s1 = self.miRuta()[0][0]
        s2 = self.miRuta()[0][1]
        if s1 != None and s2 != None:
            if s1 != None and not self.esMia(s1):
                if self.matarFicha(s1):
                    self.activarBono2()
                    try:
                        self.messageArrived.emit(
                            f"Ha matado una ficha de [{self.__names[self.obtenerOwnerIndex(s1)[0]]}] en la salida"
                        )
                    except:
                        pass
                    return True
            if s2 != None and not self.esMia(s2):
                if self.matarFicha(s2):
                    self.activarBono2()
                    try:
                        self.messageArrived.emit(
                            f"Ha matado una ficha de [{self.__names[self.obtenerOwnerIndex(s2)[0]]}] en la salida"
                        )
                    except:
                        pass
                    return True
        return False

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

    def esMia(self, ficha):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            if ficha == self.__fichas[i]:
                return True
        return False

    def tirarDados(self):
        metaIndex = len(self.miRuta()) - 1
        enJuego = 4 - Utils.contarFichas(self.miRuta()[metaIndex])
        dadoSolo = 0
        if enJuego == 1:
            restante = None
            for mFicha in self.misFichas():
                if not mFicha in self.miRuta()[metaIndex]:
                    restante = mFicha
                    break
            posI = self.obtenerPosRuta(restante)[0]
            if posI >= metaIndex - 7:
                if self.sender() == self.ui.dado1:
                    dadoSolo = 1
                elif self.sender() == self.ui.dado2:
                    dadoSolo = 2
                else:
                    dadoSolo = random.randint(1, 2)
        self.ui.dado1.setEnabled(False)
        self.ui.dado2.setEnabled(False)
        self.__dadosThread = QThread()
        self.__dadosWorker = DadosWorker(self.__dado1, self.__dado2, dadoSolo)
        self.__dadosWorker.moveToThread(self.__dadosThread)
        self.__dadosThread.started.connect(self.__dadosWorker.run)
        self.__dadosWorker.finished.connect(self.__dadosThread.quit)
        self.__dadosWorker.finished.connect(self.__dadosWorker.deleteLater)
        self.__dadosThread.finished.connect(self.__dadosThread.deleteLater)
        self.__dadosWorker.progress.connect(self.mostrarDados)
        self.__dadosWorker.finished.connect(self.onDadosGirados)
        self.__dadosThread.start()
        Sound.play(self.__sndDados)

    def mostrarDados(self, s1, s2):
        self.ui.dado1.setStyleSheet(
            f"border-image: url(:/rc/images/dados/dado{self.__turno}{s1}.png) 0 0 0 0 stretch stretch;"
        )
        self.ui.dado2.setStyleSheet(
            f"border-image: url(:/rc/images/dados/dado{self.__turno}{s2}.png) 0 0 0 0 stretch stretch;"
        )

    def onDadosGirados(self, s1, s2):
        self.__dado1 = s1
        self.__dado2 = s2
        self.mostrarDados(s1, s2)
        try:
            self.messageArrived.emit(f"Tira los dados y obtiene [{s1}:{s2}]")
        except:
            pass
        self.__dadosT = True
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
        if self.soyIA():
            self.__iaTemp = self.__ia
            self.__iaTempThread = self.__iaThread
            self.iniciarIA()

    def iniciarIA(self):
        self.__iaThread = QThread()
        self.__ia = LerchisIA(self)
        self.__ia.moveToThread(self.__iaThread)
        self.__iaThread.started.connect(self.__ia.jugar)
        self.__ia.finished.connect(self.__iaThread.quit)
        self.__ia.finished.connect(self.__ia.deleteLater)
        self.__iaThread.finished.connect(self.__iaThread.deleteLater)
        self.__iaThread.start()

    def misFichas(self):
        mias = []
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            mias.append(self.__fichas[i])
        return mias

    def miCasa(self):
        return self.__casas[self.__turno]

    def miRuta(self):
        return self.__rutas[self.__turno]

    def miDado1(self):
        return self.__dado1

    def miDado2(self):
        return self.__dado2

    def miBono1(self):
        return 10 if self.__disponibleBono1 else 0

    def miBono2(self):
        return 20 if self.__disponibleBono2 else 0

    def puedeJugar(self):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            ficha = self.__fichas[i]
            if self.estaEnCasa(ficha):
                if self.puedeSalir():
                    if (
                        self.__dado1 == 5
                        or self.__dado2 == 5
                        or self.__dado1 + self.__dado2 == 5
                    ):
                        return True
            else:
                mData = [
                    (self.__dado1 > 0, self.__dado1),
                    (self.__dado2 > 0, self.__dado2),
                    (self.__disponibleBono1, 10),
                    (self.__disponibleBono2, 20),
                ]
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
        if self.__dado1 == self.__dado2 and self.tienePuentePropio():
            p1 = self.miRuta()[0][0]
            p2 = self.miRuta()[0][1]
            if ficha != p1 and ficha != p2:
                movs = Utils.cargarJugadasPosibles(
                    self,
                    p1,
                    self.__dado1,
                    self.__dado2,
                    self.__disponibleBono1,
                    self.__disponibleBono2,
                )
                if len(movs) > 0:
                    return False
        posI = self.obtenerPosRuta(ficha)[0]
        if posI + pasos >= len(self.miRuta()):
            return False
        for j in range(len(self.miRuta()[posI + pasos])):
            if self.miRuta()[posI + pasos][j] == None and not self.hayPuenteEnMedio(
                posI, posI + pasos
            ):
                return True
        return False

    def tienePuentePropio(self):
        for f in self.miRuta()[0]:
            if f == None or not self.esMia(f):
                return False
        return True

    def hayPuenteEnMedio(self, desde, hasta):
        for i in range(len(self.__bridges)):
            pos = self.__bridges[i]
            posOwner = self.__turno + i
            posOwner -= 4 if posOwner > 3 else 0
            if desde >= pos:
                continue
            if hasta <= pos:
                break
            hayPuente = True
            for cCel in self.miRuta()[pos]:
                if cCel == None:
                    hayPuente = False
                    break
                owner = self.obtenerOwnerIndex(cCel)[0]
                if owner != posOwner:
                    hayPuente = False
                    break
            if hayPuente:
                return True
        return False

    def obtenerPosRuta(self, ficha):
        posI = 0
        posJ = 0
        for i in range(len(self.miRuta())):
            for j in range(len(self.miRuta()[i])):
                if self.miRuta()[i][j] == ficha:
                    posI = i
                    posJ = j
                    break
        return (posI, posJ)

    def matarFicha(self, ficha):
        posI, posJ = self.obtenerPosRuta(ficha)
        owner, index = self.obtenerOwnerIndex(ficha)
        if MoveUtils.moverFicha(self.miRuta(), posI, posJ, self.__casas, owner, index):
            self.relocateAll()
            return True
        return False

    def cambioDeTurno(self):
        if not self.__jugando:
            self.onPartidaTerminada()
            return
        self.__cuentaDoble = 0
        self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
        estados = [
            self.ui.checkPlayer0.isChecked(),
            self.ui.checkPlayer1.isChecked(),
            self.ui.checkPlayer2.isChecked(),
            self.ui.checkPlayer3.isChecked(),
        ]
        terminar = False
        if True in estados:
            enMeta = Utils.contarFichas(self.miRuta()[len(self.miRuta()) - 1])
            numSaltos = 0
            while not estados[self.__turno] or enMeta == 4:
                self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
                enMeta = Utils.contarFichas(self.miRuta()[len(self.miRuta()) - 1])
                numSaltos += 1
                if numSaltos >= 4:
                    terminar = True
                    break
        else:
            enMeta = Utils.contarFichas(self.miRuta()[len(self.miRuta()) - 1])
            numSaltos = 0
            while enMeta == 4:
                self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
                enMeta = Utils.contarFichas(self.miRuta()[len(self.miRuta()) - 1])
                numSaltos += 1
                if numSaltos >= 4:
                    terminar = True
                    break
        if terminar:
            self.terminarPartida()
        else:
            self.prepararDados()
            self.__repetirTirada = False
            self.__tempThread = self.__turnoThread
            self.__tempWorker = self.__turnoWorker
            self.iniciarContadorTurno(30)

    def prepararDados(self):
        self.mostrarDados(0, 0)
        self.ui.dado1.setEnabled(True)
        self.ui.dado2.setEnabled(True)
        self.__dadosT = False
        self.__dado1 = 0
        self.__dado2 = 0
        self.__disponibleBono1 = False
        self.__disponibleBono2 = False
        self.__reactivandoDados = False
        if self.soyIA():
            self.tirarDados()
        Sound.play(self.__sndTurno)

    def virarMasAdelantada(self):
        for i in range(len(self.miRuta()) - 9, -1, -1):
            for j in range(len(self.miRuta()[i])):
                ficha = self.miRuta()[i][j]
                if ficha != None and self.esMia(ficha):
                    self.matarFicha(ficha)
                    Sound.play(self.__sndMatar)
                    return True
        return False

    def nuevaPartida(self):
        self.ui.btnNuevaPartida.setEnabled(False)
        self.restablecerTablero()
        self.__dado1 = 0
        self.__dado2 = 0
        estados = [
            self.ui.checkPlayer0.isChecked(),
            self.ui.checkPlayer1.isChecked(),
            self.ui.checkPlayer2.isChecked(),
            self.ui.checkPlayer3.isChecked(),
        ]
        active = []
        if True in estados:
            for i in range(len(estados)):
                if estados[i]:
                    active.append(i)
        else:
            active = [0, 1, 2, 3]
        self.__turno = (
            active[random.randint(0, len(active) - 1)] if len(active) > 1 else active[0]
        )
        self.mostrarDados(0, 0)
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__jugando = True
        self.__dadosT = False
        self.ui.dado1.setEnabled(True)
        self.ui.dado2.setEnabled(True)
        self.ui.checkPlayer0.setEnabled(False)
        self.ui.checkPlayer1.setEnabled(False)
        self.ui.checkPlayer2.setEnabled(False)
        self.ui.checkPlayer3.setEnabled(False)
        self.ui.checkIA0.setEnabled(False)
        self.ui.checkIA1.setEnabled(False)
        self.ui.checkIA2.setEnabled(False)
        self.ui.checkIA3.setEnabled(False)
        self.ui.btnTerminarPartida.setEnabled(True)
        self.prepararDados()
        self.iniciarContadorTurno(30)
        Music.stop()
        Music.unload()
        Music.load(os.path.join("sounds", "music2.wav"))
        Music.play(-1, 0, 250)

    def terminarPartida(self):
        self.ui.btnTerminarPartida.setEnabled(False)
        self.__cuentaDoble = 0
        self.__repetirTirada = False
        self.__jugando = False
        self.__dadosT = False
        self.ui.dado1.setEnabled(False)
        self.ui.dado2.setEnabled(False)
        if self.__contandoTurno:
            self.__turnoWorker.faster()
        else:
            self.onPartidaTerminada()

    def onPartidaTerminada(self):
        self.ui.checkPlayer0.setEnabled(True)
        self.ui.checkPlayer1.setEnabled(True)
        self.ui.checkPlayer2.setEnabled(True)
        self.ui.checkPlayer3.setEnabled(True)
        self.ui.checkIA0.setEnabled(True)
        self.ui.checkIA1.setEnabled(True)
        self.ui.checkIA2.setEnabled(True)
        self.ui.checkIA3.setEnabled(True)
        self.ui.btnNuevaPartida.setEnabled(True)
        Music.stop()
        Music.unload()
        Music.load(os.path.join("sounds", "music1.wav"))
        Music.play(-1, 0, 250)

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
        if (
            self.__dadosT
            and not self.__turnoWorker.isFast()
            and not self.__reactivandoDados
            and not self.puedeJugar()
        ):
            if self.__repetirTirada:
                self.__repetirTirada = False
                self.iniciarReactivadorDados()
            else:
                if self.__contandoTurno:
                    self.__turnoWorker.faster()

    def onContadorTurnoFinished(self, value):
        self.onContadorTurnoProgress(value)
        self.__contandoTurno = False
        self.cambioDeTurno()

    def iniciarReactivadorDados(self):
        self.__reactivandoDados = True
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
            QListWidgetItem(
                self.__icons[self.__turno], f"[{self.__names[self.__turno]}]: {msg}."
            )
        )
        count = self.ui.listHistorial.count()
        while count > 1024:
            self.ui.listHistorial.takeItem(0)
            count = self.ui.listHistorial.count()
        self.ui.listHistorial.setCurrentRow(count - 1)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))
application = Ventana()
application.show()
sys.exit(app.exec())
