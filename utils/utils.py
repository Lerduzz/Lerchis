from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import (
    QProxyStyle,
    QStyle,
    QStyleOption,
    QMenu,
    QAction,
    QWidget,
    QToolButton,
)
from utils.static import AuxStatic


class EstiloIconos(QProxyStyle):
    def __init__(self, size: int):
        super().__init__()
        self.__size = size

    def pixelMetric(self, metric, option: QStyleOption = 0, widget: QWidget = 0) -> int:
        if metric == QStyle.PM_SmallIconSize:
            return self.__size
        return super().pixelMetric(metric, option, widget)


class Utils:
    @staticmethod
    def contarFichas(lista: list) -> int:
        count = 0
        for f in lista:
            if f != None:
                count += 1
        return count

    @staticmethod
    def crearMenuContextual(
        parent,
        sender: QToolButton,
        turno: int,
        dado1: int,
        dado2: int,
        dado1Disp: bool,
        dado2Disp: bool,
        bono1Disp: bool,
        bono2Disp: bool,
    ):
        menu = QMenu(parent)
        font = AuxStatic.fontMenu()
        menu.setStyle(EstiloIconos(sender.width()))
        count = 0
        iconDado1 = AuxStatic.iconoMenu(turno, dado1)
        actionDado1 = QAction(iconDado1, "Primer dado")
        actionDado1.setFont(font)
        iconDado2 = AuxStatic.iconoMenu(turno, dado2)
        actionDado2 = QAction(iconDado2, "Segundo dado")
        actionDado2.setFont(font)
        iconBonus1 = AuxStatic.iconoMenu(turno, 10, "s")
        actionBonus1 = QAction(iconBonus1, "Bono por llegar")
        actionBonus1.setFont(font)
        iconBonus2 = AuxStatic.iconoMenu(turno, 20, "s")
        actionBonus2 = QAction(iconBonus2, "Bono por matar")
        actionBonus2.setFont(font)
        sumDados = dado1 + dado2
        iconDado1Dado2 = AuxStatic.iconoMenu(turno, sumDados, "s")
        actionDado1Dado2 = QAction(iconDado1Dado2, "Todos los dados")
        actionDado1Dado2.setFont(font)
        iconDado1Bonus1 = AuxStatic.iconoMenu(turno, dado1 + 10, "s")
        actionDado1Bonus1 = QAction(iconDado1Bonus1, "Primer dado + Bono por llegar")
        actionDado1Bonus1.setFont(font)
        iconDado1Bonus2 = AuxStatic.iconoMenu(turno, dado1 + 20, "s")
        actionDado1Bonus2 = QAction(iconDado1Bonus2, "Primer dado + Bono por matar")
        actionDado1Bonus2.setFont(font)
        iconDado2Bonus1 = AuxStatic.iconoMenu(turno, dado2 + 10, "s")
        actionDado2Bonus1 = QAction(iconDado2Bonus1, "Segundo dado + Bono por llegar")
        actionDado2Bonus1.setFont(font)
        iconDado2Bonus2 = AuxStatic.iconoMenu(turno, dado2 + 20, "s")
        actionDado2Bonus2 = QAction(iconDado2Bonus2, "Segundo dado + Bono por matar")
        actionDado2Bonus2.setFont(font)
        iconBonus1Bonus2 = AuxStatic.iconoMenu(turno, 30, "s")
        actionBonus1Bonus2 = QAction(iconBonus1Bonus2, "Todos los bonos")
        actionBonus1Bonus2.setFont(font)
        if dado1Disp:
            if parent.estaEnCasa(sender):
                if dado1 == 5 and parent.puedeSalir():
                    menu.addAction(actionDado1)
                    count += 1
            else:
                if parent.puedeMover(sender, dado1):
                    menu.addAction(actionDado1)
                    count += 1
        if dado2Disp:
            if parent.estaEnCasa(sender):
                if dado2 == 5 and parent.puedeSalir():
                    menu.addAction(actionDado2)
                    count += 1
            else:
                if parent.puedeMover(sender, dado2):
                    menu.addAction(actionDado2)
                    count += 1
        if bono1Disp:
            if not parent.estaEnCasa(sender) and parent.puedeMover(sender, 10):
                menu.addAction(actionBonus1)
                count += 1
        if bono2Disp:
            if not parent.estaEnCasa(sender) and parent.puedeMover(sender, 20):
                menu.addAction(actionBonus2)
                count += 1
        if dado1Disp and dado2Disp:
            if parent.estaEnCasa(sender):
                if sumDados == 5 and parent.puedeSalir():
                    menu.addAction(actionDado1Dado2)
                    count += 1
            else:
                if parent.puedeMover(sender, sumDados):
                    menu.addAction(actionDado1Dado2)
                    count += 1
        if dado1Disp and bono1Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado1 + 10):
                    menu.addAction(actionDado1Bonus1)
                    count += 1
        if dado1Disp and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado1 + 20):
                    menu.addAction(actionDado1Bonus2)
                    count += 1
        if dado2Disp and bono1Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado2 + 10):
                    menu.addAction(actionDado2Bonus1)
                    count += 1
        if dado2Disp and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado2 + 20):
                    menu.addAction(actionDado2Bonus2)
                    count += 1
        if bono1Disp and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, 30):
                    menu.addAction(actionBonus1Bonus2)
                    count += 1
        if count > 0:
            pos = QPoint(sender.x() + sender.width(), sender.y())
            actionR = menu.exec_(parent.mapToGlobal(pos))
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

    @staticmethod
    def cargarJugadasPosibles(
        parent,
        sender: QToolButton,
        dado1: int,
        dado2: int,
        bono1Disp: bool,
        bono2Disp: bool,
    ):
        posibles = []
        if dado1 > 0:
            if parent.estaEnCasa(sender):
                if dado1 == 5 and parent.puedeSalir():
                    posibles.append([1])
            else:
                if parent.puedeMover(sender, dado1):
                    posibles.append([1])
        if dado2 > 0:
            if parent.estaEnCasa(sender):
                if dado2 == 5 and parent.puedeSalir():
                    posibles.append([2])
            else:
                if parent.puedeMover(sender, dado2):
                    posibles.append([2])
        if bono1Disp:
            if not parent.estaEnCasa(sender) and parent.puedeMover(sender, 10):
                posibles.append([3])
        if bono2Disp:
            if not parent.estaEnCasa(sender) and parent.puedeMover(sender, 20):
                posibles.append([4])
        if dado1 > 0 and dado2 > 0:
            if parent.estaEnCasa(sender):
                if dado1 + dado2 == 5 and parent.puedeSalir():
                    posibles.append([1, 2])
            else:
                if parent.puedeMover(sender, dado1 + dado2):
                    posibles.append([1, 2])
        if dado1 > 0 and bono1Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado1 + 10):
                    posibles.append([1, 3])
        if dado1 > 0 and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado1 + 20):
                    posibles.append([1, 4])
        if dado2 > 0 and bono1Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado2 + 10):
                    posibles.append([2, 3])
        if dado2 > 0 and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, dado2 + 20):
                    posibles.append([2, 4])
        if bono1Disp and bono2Disp:
            if not parent.estaEnCasa(sender):
                if parent.puedeMover(sender, 30):
                    posibles.append([3, 4])
        return posibles

    @staticmethod
    def puedeUsarFicha(parent, jugando: bool, tirados: bool, sender: QToolButton):
        return jugando and tirados and parent.esMia(sender) and not parent.soyIA()
