from PyQt5.QtCore import QObject, pyqtSignal


class LerchisIA(QObject):
    dado1Usado = pyqtSignal()
    dado2Usado = pyqtSignal()
    bono1Usado = pyqtSignal()
    bono2Usado = pyqtSignal()
    terminado = pyqtSignal()
    haLlegado = pyqtSignal()
    haMatado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.haLlegado.connect(self.updateBonus1)
        self.haMatado.connect(self.updateBonus2)

    def updateBonus1(self):
        self.__b1 = 10
    
    def updateBonus2(self):
        self.__b2 = 20

    def hayMovimientosDisponibles(self):
        return True

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
                if self.salirDeCasa(f):
                    if self.__d1 == 5:
                        self.dado1Usado.emit()
                        self.__d1 = 0
                    elif self.__d2 == 5:
                        self.dado2Usado.emit()
                        self.__d2 = 0
                    else:
                        self.dado1Usado.emit()
                        self.__d1 = 0
                        self.dado2Usado.emit()
                        self.__d2 = 0
                    return True
        return False

    def intentaPonerseASalvo(self):
        return False

    def moverLoMasLejosPosible(self, fichas):
        movFichas = []
        for f in fichas:
            movs = self.cargarJugadasPosibles(f)
            if movs == None:
                continue
            movMax = 0
            rowMax = []
            for row in movs:
                movCurrent = 0
                for mov in row:
                    if mov == 1:
                        movCurrent += self.__d1
                    elif mov == 2:
                        movCurrent += self.__d2
                    elif mov == 3:
                        movCurrent += self.__b1
                    elif mov == 4:
                        movCurrent += self.__b2
                # TODO: IF PUEDE_MOVER
                if movCurrent > movMax:
                    movMax = movCurrent
                    rowMax = row
            if movMax == 0:
                continue
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
            self.moverFichaAutomatico(mfFicha, mfMovs)
            for x in mfMovs:
                if x == 1:
                    self.dado1Usado.emit()
                    self.__d1 = 0
                elif x == 2:
                    self.dado2Usado.emit()
                    self.__d2 = 0
                elif x == 3:
                    self.bono1Usado.emit()
                    self.__b1 = 0
                elif x == 4:
                    self.bono2Usado.emit()
                    self.__b2 = 0
            return True
        return False

    def jugar(
        self,
        d1,
        d2,
        b1,
        b2,
        fichas: list,
        casa: list,
        puedeJugar,
        salirDeCasa,
        cargarJugadasPosibles,
        moverFichaAutomatico,
    ):
        self.__d1 = d1
        self.__d2 = d2
        self.__b1 = b1
        self.__b2 = b2
        self.puedeJugar = puedeJugar
        self.salirDeCasa = salirDeCasa
        self.cargarJugadasPosibles = cargarJugadasPosibles
        self.moverFichaAutomatico = moverFichaAutomatico
        while puedeJugar():
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
