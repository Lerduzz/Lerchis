from PyQt5.QtCore import QObject
from utils.utils import Utils
from utils.move import MoveUtils
from utils.static import InitStatic


class LerchisIA(QObject):
    def intentaMatarOtraFicha(self):
        # Recorrer las fichas del usuario.
        # Obtener posibles moviemientos para cada ficha.
        # Comprobar para cada movimiento si se come en este.
        # Efectuarlo y retornar | o seguir.
        return False

    def intentaEntrarEnMeta(self):
        return False

    def intentaSacarFicha(self):
        if (
            self.__parent.miDado1() != 5
            and self.__parent.miDado2() != 5
            and self.__parent.miDado1() + self.__parent.miDado2() != 5
        ):
            return False
        for f in self.__parent.miCasa():
            if f != None:
                if self.__parent.intentaSalirDeCasa(f):
                    return True
        return False

    def intentaPonerseASalvo(self):
        return False

    def moverLoMasLejosPosible(self):
        movFichas = []
        for f in self.__parent.misFichas():
            movs = Utils.cargarJugadasPosibles(
                self.__parent,
                f,
                self.__parent.miDado1(),
                self.__parent.miDado2(),
                self.__parent.miBono1(),
                self.__parent.miBono2(),
            )
            if len(movs) == 0:
                continue
            movMax = 0
            rowMax = MoveUtils.mayorDistancia(movs, self.__parent.miDado1(), self.__parent.miDado2())
            for mov in rowMax:
                if mov == 1:
                    movMax += self.__parent.miDado1()
                elif mov == 2:
                    movMax += self.__parent.miDado2()
                elif mov == 3:
                    movMax += self.__parent.miBono1()
                elif mov == 4:
                    movMax += self.__parent.miBono2()
            movFichas.append((movMax, rowMax, f))
        mfMax = 0
        mfMovs = []
        mfFicha = None
        for m, ml, f in movFichas:
            if mfMax < m:
                mfMax = m
                mfMovs = ml
                mfFicha = f
        if mfMax > 0 and mfFicha != None:
            MoveUtils.moverFichaDirecto(
                self.__parent,
                mfFicha,
                mfMovs,
                self.__parent.miDado1(),
                self.__parent.miDado2(),
                self.__parent.miBono1(),
                self.__parent.miBono2(),
                self.__parent.miRuta(),
                InitStatic.excluir(),
            )
            return True
        return False

    def jugar(self, parent):
        self.__parent = parent
        while parent.puedeJugar():
            if self.intentaMatarOtraFicha():
                continue
            if self.intentaEntrarEnMeta():
                continue
            if self.intentaSacarFicha():
                continue
            if self.intentaPonerseASalvo():
                continue
            if self.moverLoMasLejosPosible():
                continue
            break
