from PyQt5.QtWidgets import QToolButton
from utils.static import InitStatic
from utils.utils import Utils


class MoveUtils:
    @staticmethod
    def moverFicha(desde: list, iD: int, jD: int, hasta: list, iH: int, jH: int):
        if desde[iD][jD] == None or hasta[iH][jH] != None:
            return False
        temp = hasta[iH][jH]
        hasta[iH][jH] = desde[iD][jD]
        desde[iD][jD] = temp
        return True

    @staticmethod
    def moverFichaDirecto(
        parent,
        ficha: QToolButton,
        mov: list,
        d1: int,
        d2: int,
        b1: bool,
        b2: bool,
        ruta: list,
        excl: list,
    ):
        total = 0
        total += d1 if 1 in mov else 0
        total += d2 if 2 in mov else 0
        total += 10 if b1 and 3 in mov else 0
        total += 20 if b2 and 4 in mov else 0
        if total == 0:
            return
        posI, posJ = parent.obtenerPosRuta(ficha)
        if posI + total >= len(ruta):
            return
        for j in range(len(ruta[posI + total])):
            dest = ruta[posI + total][j]
            if dest == None and not parent.hayPuenteEnMedio(posI, posI + total):
                if not MoveUtils.moverFicha(
                    ruta,
                    posI,
                    posJ,
                    ruta,
                    posI + total,
                    j,
                ):
                    continue
                parent.relocateAll()
                if 1 in mov:
                    parent.dado1Usado()
                if 2 in mov:
                    parent.dado2Usado()
                if 3 in mov:
                    parent.bono1Usado()
                if 4 in mov:
                    parent.bono2Usado()
                parent.sonidoMover()
                rplr = "s" if total > 1 else ""
                rmsg = f"Camina un total de {total} paso{rplr}"
                for jC in range(len(ruta[posI + total])):
                    fM = ruta[posI + total][jC]
                    if (
                        j != jC
                        and fM != None
                        and not posI + total in excl
                        and not parent.esMia(fM)
                    ):
                        if parent.matarFicha(fM):
                            parent.activarBono2()
                            rmsg += f" y mata una ficha de [{InitStatic.names()[parent.obtenerOwnerIndex(fM)[0]]}]"
                            break
                if posI + total == len(ruta) - 1:
                    parent.activarBono1()
                    rmsg += " y llega a la meta"
                try:
                    parent.messageArrived.emit(rmsg)
                except:
                    pass
                break

    @staticmethod
    def calcularPosicionCasilla(
        x: int, y: int, o: int, i: int, h: int, hC: int, hF: int
    ):
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
    def mayorDistancia(movs: list, d1: int, d2: int) -> list:
        movMax = 0
        rowMax = movs[0]
        for row in movs:
            movCurrent = 0
            for mov in row:
                if mov == 1:
                    movCurrent += d1
                elif mov == 2:
                    movCurrent += d2
                elif mov == 3:
                    movCurrent += 10
                elif mov == 4:
                    movCurrent += 20
            if movCurrent > movMax:
                movMax = movCurrent
                rowMax = row
        return rowMax
