from PyQt5.QtCore import QObject, pyqtSignal
from utils.utils import Utils
from utils.move import MoveUtils
from utils.static import InitStatic


class LerchisIA(QObject):
    dado1Usado = pyqtSignal()
    dado2Usado = pyqtSignal()
    bono1Usado = pyqtSignal()
    bono2Usado = pyqtSignal()
    terminado = pyqtSignal()
    usarDado1 = pyqtSignal()
    usarDado2 = pyqtSignal()
    haLlegado = pyqtSignal()
    haMatado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.usarDado1.connect(self.updateDado1)
        self.usarDado2.connect(self.updateDado2)
        self.haLlegado.connect(self.updateBonus1)
        self.haMatado.connect(self.updateBonus2)

    def updateDado1(self):
        self.__d1 = 0

    def updateDado2(self):
        self.__d2 = 0

    def updateBonus1(self):
        self.__b1 = 10

    def updateBonus2(self):
        self.__b2 = 20

    def intentaMatarOtraFicha(self, fichas):
        # Recorrer las fichas del usuario.
        # Obtener posibles moviemientos para cada ficha.
        # Comprobar para cada movimiento si se come en este.
        # Efectuarlo y retornar | o seguir.
        return False

    def intentaEntrarEnMeta(self):
        return False

    def intentaSacarFicha(self, casa: list):
        if self.__d1 != 5 and self.__d2 != 5 and self.__d1 + self.__d2 != 5:
            return False
        for f in casa:
            if f != None:
                if self.__parent.intentaSalirDeCasa(f):
                    return True
        return False

    def intentaPonerseASalvo(self):
        return False

    def moverLoMasLejosPosible(self, fichas):
        movFichas = []
        for f in fichas:
            movs = Utils.cargarJugadasPosibles(
                self.__parent,
                f,
                self.__d1,
                self.__d2,
                self.__b1,
                self.__b2,
            )
            if len(movs) == 0:
                continue
            movMax = 0
            rowMax = MoveUtils.mayorDistancia(movs, self.__d1, self.__d2)
            for mov in rowMax:
                if mov == 1:
                    movMax += self.__d1
                elif mov == 2:
                    movMax += self.__d2
                elif mov == 3:
                    movMax += self.__b1
                elif mov == 4:
                    movMax += self.__b2
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
                self.__d1,
                self.__d2,
                self.__b1,
                self.__b2,
                self.__ruta,
                InitStatic.excluir(),
            )
            for x in mfMovs:
                if x == 1:
                    self.dado1Usado.emit()
                elif x == 2:
                    self.dado2Usado.emit()
                elif x == 3:
                    self.bono1Usado.emit()
                    self.__b1 = 0
                elif x == 4:
                    self.bono2Usado.emit()
                    self.__b2 = 0
            return True
        return False

    def jugar(self, parent, d1, d2, b1, b2, fichas: list, casa: list, ruta: list):
        self.__parent = parent
        self.__d1 = d1
        self.__d2 = d2
        self.__b1 = b1
        self.__b2 = b2
        self.__ruta = ruta
        while parent.puedeJugar():
            if self.intentaMatarOtraFicha(fichas):
                continue
            if self.intentaEntrarEnMeta():
                continue
            if self.intentaSacarFicha(casa):
                continue
            if self.intentaPonerseASalvo():
                continue
            if self.moverLoMasLejosPosible(fichas):
                continue
            break
        self.terminado.emit()
