from PyQt5.QtWidgets import QProxyStyle, QStyle

class EstiloIconos(QProxyStyle):
    def __init__(self, size):
        super().__init__()
        self.__size = size

    def pixelMetric(self, metric, option = 0, widget = 0):
        if metric == QStyle.PM_SmallIconSize:
            return self.__size
        return super().pixelMetric(metric, option, widget)


class Utils:
    def moverFicha(desde, iD, jD, hasta, iH, jH):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True

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
