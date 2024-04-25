import sys
import qdarkstyle
from PyQt5.QtCore import QPoint, QThread, Qt
from PyQt5.QtGui import QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMenu, QAction
from parchis_ui import Ui_VentanaJuego
from workers.dados import DadosWorker, ReactivarWorker
from workers.turno import TurnoWorker
from utils.utils import EstiloIconos, Utils
from utils.static import InitStatic, AuxStatic


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
        self.__fichas = InitStatic.fichas(self.ui, self.jugarFicha)
        self.__posCaminos = InitStatic.posCaminos()
        self.__posMetas = InitStatic.posMetas()
        self.__excluir = InitStatic.excluir()
        self.__bridges = InitStatic.bridges()
        self.__names = InitStatic.names()
        self.__icons = InitStatic.icons()
        self.restablecerTablero()
        self.__jugando = False
        self.__dadosTirados = False
        self.__disponibleDado1 = False
        self.__disponibleDado2 = False
        self.__disponibleBonusMatar = False
        self.__disponibleBonusLlegar = False
        self.__contandoTurno = False

    def restablecerTablero(self):
        self.__casas = InitStatic.casas(self.ui)
        self.__caminos = InitStatic.caminos()
        self.__metas = InitStatic.metas()
        self.__rutas = InitStatic.rutas(self.__caminos, self.__metas)
        self.relocateAll()

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.resizeAll()
        self.relocateAll()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif e.key() == Qt.Key.Key_Escape:
            if self.isFullScreen() or self.isMaximized():
                self.showNormal()

    def abrirMenu(self, sender):
        menu = QMenu(self)
        font = AuxStatic.fontMenu()
        menu.setStyle(EstiloIconos(sender.width()))
        count = 0
        iconDado1 = AuxStatic.iconoMenu(self.__turno, self.__dado1)
        actionDado1 = QAction(iconDado1, "Primer dado")
        actionDado1.setFont(font)
        iconDado2 = AuxStatic.iconoMenu(self.__turno, self.__dado2)
        actionDado2 = QAction(iconDado2, "Segundo dado")
        actionDado2.setFont(font)
        iconBonus1 = AuxStatic.iconoMenu(self.__turno, 10, "s")
        actionBonus1 = QAction(iconBonus1, "Bono por llegar")
        actionBonus1.setFont(font)
        iconBonus2 = AuxStatic.iconoMenu(self.__turno, 20, "s")
        actionBonus2 = QAction(iconBonus2, "Bono por matar")
        actionBonus2.setFont(font)
        sumDados = self.__dado1 + self.__dado2
        iconDado1Dado2 = AuxStatic.iconoMenu(self.__turno, sumDados, "s")
        actionDado1Dado2 = QAction(iconDado1Dado2, "Todos los dados")
        actionDado1Dado2.setFont(font)
        iconDado1Bonus1 = AuxStatic.iconoMenu(self.__turno, self.__dado1 + 10, "s")
        actionDado1Bonus1 = QAction(iconDado1Bonus1, "Primer dado + Bono por llegar")
        actionDado1Bonus1.setFont(font)
        iconDado1Bonus2 = AuxStatic.iconoMenu(self.__turno, self.__dado1 + 20, "s")
        actionDado1Bonus2 = QAction(iconDado1Bonus2, "Primer dado + Bono por matar")
        actionDado1Bonus2.setFont(font)
        iconDado2Bonus1 = AuxStatic.iconoMenu(self.__turno, self.__dado2 + 10, "s")
        actionDado2Bonus1 = QAction(iconDado2Bonus1, "Segundo dado + Bono por llegar")
        actionDado2Bonus1.setFont(font)
        iconDado2Bonus2 = AuxStatic.iconoMenu(self.__turno, self.__dado2 + 20, "s")
        actionDado2Bonus2 = QAction(iconDado2Bonus2, "Segundo dado + Bono por matar")
        actionDado2Bonus2.setFont(font)
        iconBonus1Bonus2 = AuxStatic.iconoMenu(self.__turno, 30, "s")
        actionBonus1Bonus2 = QAction(iconBonus1Bonus2, "Todos los bonos")
        actionBonus1Bonus2.setFont(font)
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
                if sumDados == 5 and self.puedeSalir():
                    menu.addAction(actionDado1Dado2)
                    count += 1
            else:
                if self.puedeMover(sender, sumDados):
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
                        xR, yR = Utils.calcularPosicionCasilla(
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
                                xR, yR = Utils.calcularPosicionCasilla(
                                    x, y, o, k, h, hCasilla, hFicha
                                )
                                self.__metas[i][j][k].move(xR, yR)

    def tirarDados(self):
        enJuego = 4 - Utils.contarFichas(
            self.__rutas[self.__turno][len(self.__rutas[self.__turno]) - 1]
        )
        dadoSolo = 0
        if enJuego == 1:
            rectaFinal = False
            metaIndex = len(self.__rutas[self.__turno]) - 1
            for i in range(metaIndex - 6, metaIndex):
                for f in self.__rutas[self.__turno][i]:
                    if f != None and self.esMia(f):
                        rectaFinal = True
            if rectaFinal:
                if self.sender() == self.ui.dado1:
                    dadoSolo = 1
                if self.sender() == self.ui.dado2:
                    dadoSolo = 2
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

    def mostrarDados(self, s1, s2):
        self.ui.dado1.setStyleSheet(
            f"border-image: url(:/dados/dado{self.__turno}{s1}.png) 0 0 0 0 stretch stretch;"
        )
        self.ui.dado2.setStyleSheet(
            f"border-image: url(:/dados/dado{self.__turno}{s2}.png) 0 0 0 0 stretch stretch;"
        )

    def onDadosGirados(self, s1, s2):
        self.insertarMensaje(f"Tira los dados y saca [{s1}]:[{s2}]")
        self.__dado1 = s1
        self.__dado2 = s2
        self.mostrarDados(s1, s2)
        self.__dadosTirados = True
        self.__disponibleDado1 = self.__dado1 > 0
        self.__disponibleDado2 = self.__dado2 > 0
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
                self.insertarMensaje(
                    "Sin movimientos disponibles, vuelve a tirar los dados"
                )
            else:
                if self.__contandoTurno:
                    self.__turnoWorker.faster()
                self.insertarMensaje("Sin movimientos disponibles, terminando turno")

    def puedeJugar(self):
        for i in range(self.__turno * 4, self.__turno * 4 + 4):
            ficha = self.__fichas[i]
            if self.estaEnCasa(ficha):
                if self.puedeSalir():
                    if (
                        (self.__disponibleDado1 and self.__dado1 == 5)
                        or (self.__disponibleDado2 and self.__dado2 == 5)
                        or (
                            self.__disponibleDado1
                            and self.__disponibleDado2
                            and self.__dado1 + self.__dado2 == 5
                        )
                    ):
                        return True
            else:
                mData = [
                    (self.__disponibleDado1, self.__dado1),
                    (self.__disponibleDado2, self.__dado2),
                    (self.__disponibleBonusLlegar, 10),
                    (self.__disponibleBonusMatar, 20),
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
        posI, posJ = self.obtenerPosRuta(ficha)
        if posI + pasos >= len(self.__rutas[self.__turno]):
            return False
        for j in range(len(self.__rutas[self.__turno][posI + pasos])):
            if self.__rutas[self.__turno][posI + pasos][
                j
            ] == None and not self.hayPuenteEnMedio(posI, posI + pasos):
                return True
        return False

    def puedeSalir(self):
        s1 = self.__rutas[self.__turno][0][0]
        s2 = self.__rutas[self.__turno][0][1]
        return (
            False
            if s1 != None and s2 != None and self.esMia(s1) and self.esMia(s2)
            else True
        )

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
            for j in range(len(self.__rutas[self.__turno][pos])):
                if self.__rutas[self.__turno][pos][j] == None:
                    hayPuente = False
                    break
                owner, index = self.obtenerOwnerIndex(
                    self.__rutas[self.__turno][pos][j]
                )
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
        if (
            not self.__jugando
            or not self.__dadosTirados
            or not self.esMia(self.sender())
        ):
            return
        menuResp = self.detectarJugadaAutomatica(self.sender())
        if menuResp == None:
            menuResp = self.abrirMenu(self.sender())
            if (
                not self.__jugando
                or not self.__dadosTirados
                or not self.esMia(self.sender())
                or len(menuResp) == 0
            ):
                return
        if self.estaEnCasa(self.sender()):
            if self.puedeSalir():
                if self.__disponibleDado1 and 1 in menuResp and self.__dado1 == 5:
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado1 = False
                        self.insertarMensaje("Saca una ficha con el primer dado")
                elif self.__disponibleDado2 and 2 in menuResp and self.__dado2 == 5:
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado2 = False
                        self.insertarMensaje("Saca una ficha con el segundo dado")
                elif (
                    self.__disponibleDado1
                    and self.__disponibleDado2
                    and 1 in menuResp
                    and 2 in menuResp
                    and self.__dado1 + self.__dado2 == 5
                ):
                    if self.salirDeCasa(self.sender()):
                        self.__disponibleDado1 = False
                        self.__disponibleDado2 = False
                        self.insertarMensaje("Saca una ficha con ambos dados")
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
                        if self.__rutas[self.__turno][posI + total][
                            j
                        ] == None and not self.hayPuenteEnMedio(posI, posI + total):
                            if Utils.moverFicha(
                                self.__rutas[self.__turno],
                                posI,
                                posJ,
                                self.__rutas[self.__turno],
                                posI + total,
                                j,
                            ):
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
                                for jC in range(
                                    len(self.__rutas[self.__turno][posI + total])
                                ):
                                    fM = self.__rutas[self.__turno][posI + total][jC]
                                    if (
                                        j != jC
                                        and fM != None
                                        and not posI + total in self.__excluir
                                        and not self.esMia(fM)
                                    ):
                                        if self.matarFicha(fM):
                                            self.__disponibleBonusMatar = True
                                            mFicha = fM
                                if posI + total == len(self.__rutas[self.__turno]) - 1:
                                    self.__disponibleBonusLlegar = True
                                    llego = True
                                pL = "s" if total > 1 else ""
                                if mFicha != None:
                                    oFicha, iFicha = self.obtenerOwnerIndex(mFicha)
                                    self.insertarMensaje(
                                        f"Mata una ficha del jugador [{self.__names[oFicha]}] con {total} paso{pL}"
                                    )
                                elif llego:
                                    self.insertarMensaje(
                                        f"Entra en la casilla de meta con {total} paso{pL}"
                                    )
                                else:
                                    self.insertarMensaje(
                                        f"Camina un total de {total} paso{pL}"
                                    )
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
            if Utils.moverFicha(
                self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 0
            ):
                self.relocateAll()
                return True
        elif s2 == None:
            if Utils.moverFicha(
                self.__casas, self.__turno, pos, self.__rutas[self.__turno], 0, 1
            ):
                self.relocateAll()
                return True
        return False

    def matarFicha(self, ficha):
        posI, posJ = self.obtenerPosRuta(ficha)
        owner, index = self.obtenerOwnerIndex(ficha)
        if Utils.moverFicha(
            self.__rutas[self.__turno], posI, posJ, self.__casas, owner, index
        ):
            self.relocateAll()
            return True
        return False

    def cambioDeTurno(self):
        if not self.__jugando:
            return
        self.insertarMensaje(">>>========>> TURNO TERMINADO")
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
            enMeta = Utils.contarFichas(
                self.__rutas[self.__turno][len(self.__rutas[self.__turno]) - 1]
            )
            numSaltos = 0
            while not estados[self.__turno] or enMeta == 4:
                self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
                enMeta = Utils.contarFichas(
                    self.__rutas[self.__turno][len(self.__rutas[self.__turno]) - 1]
                )
                numSaltos += 1
                if numSaltos >= 4:
                    terminar = True
                    break
        else:
            enMeta = Utils.contarFichas(
                self.__rutas[self.__turno][len(self.__rutas[self.__turno]) - 1]
            )
            numSaltos = 0
            while enMeta == 4:
                self.__turno = 0 if self.__turno >= 3 else self.__turno + 1
                enMeta = Utils.contarFichas(
                    self.__rutas[self.__turno][len(self.__rutas[self.__turno]) - 1]
                )
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
        self.restablecerTablero()
        self.__dado1 = 0
        self.__dado2 = 0
        self.__turno = 0
        self.mostrarDados(0, 0)
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
            QListWidgetItem(
                self.__icons[self.__turno], f"[{self.__names[self.__turno]}]: {msg}."
            )
        )
        count = self.ui.listHistorial.count()
        while count > 1024:
            self.ui.listHistorial.takeItem(0)
            count = self.ui.listHistorial.count()
        self.ui.listHistorial.setCurrentRow(count - 1)


app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))
application = Ventana()
application.show()
sys.exit(app.exec())
