from PyQt5.QtWidgets import QProxyStyle, QStyle, QMenu, QAction
from utils.static import AuxStatic
from utils.utils import EstiloIconos


class EstiloIconos(QProxyStyle):
    def __init__(self, size):
        super().__init__()
        self.__size = size

    def pixelMetric(self, metric, option=0, widget=0):
        if metric == QStyle.PM_SmallIconSize:
            return self.__size
        return super().pixelMetric(metric, option, widget)


class Utils:
    @staticmethod
    def contarFichas(lista):
        count = 0
        for f in lista:
            if f != None:
                count += 1
        return count

    @staticmethod
    def moverFicha(desde, iD, jD, hasta, iH, jH):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True

    @staticmethod
    def calcularPosicionCasilla(x, y, o, i, h, hC, hF):
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
            yR = (
                dY - hF - hC // 2 + hF // 4
                if i == 0
                else dY - hF - hC // 2 - hF // 2 - hF // 10
            )
        elif o == 6:
            xR = dX + hF if i == 0 else dX + hF * 2 - hF // 3
            yR = dY - hF * 2 if i == 0 else dY - hF * 3 + hF // 3
        elif o == 7:
            xR = dX + hC // 2 - hF // 4 if i == 0 else dX + hC // 2 + hF // 2 + hF // 10
            yR = dY - hF if i == 0 else dY - hF - hF // 2
        elif o == 8:
            xR = (
                dX - hF - hC // 2 + hF // 4
                if i == 0
                else dX - hF - hC // 2 - hF // 2 - hF // 10
            )
            yR = dY - hF if i == 0 else dY - hF - hF // 2
        elif o == 9:
            xR = dX - hF * 2 if i == 0 else dX - hF * 3 + hF // 3
            yR = dY - hF * 2 if i == 0 else dY - hF * 3 + hF // 3
        elif o == 10:
            xR = dX - hF if i == 0 else dX - hF - hF // 2
            yR = (
                dY - hF - hC // 2 + hF // 4
                if i == 0
                else dY - hF - hC // 2 - hF // 2 - hF // 10
            )
        elif o == 11:
            xR = dX - hF if i == 0 else dX - hF - hF // 2
            yR = dY + hC // 2 - hF // 4 if i == 0 else dY + hC // 2 + hF // 2 + hF // 10
        elif o == 12:
            xR = dX - hF * 2 if i == 0 else dX - hF * 3 + hF // 3
            yR = dY + hF if i == 0 else dY + hF * 2 - hF // 3
        elif o == 13:
            xR = (
                dX - hF - hC // 2 + hF // 4
                if i == 0
                else dX - hF - hC // 2 - hF // 2 - hF // 10
            )
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
    
    @staticmethod
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
