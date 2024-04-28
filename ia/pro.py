from PyQt5.QtCore import QObject
from utils.utils import Utils
from utils.move import MoveUtils
from utils.static import InitStatic


class LerchisIA(QObject):
    # PRIORIDAD 0: Matar en la salida.
    def intentaMatarEnSalida(self):
        # SIN EXCEPCIONES!
        if (
            self.__parent.miDado1() != 5
            and self.__parent.miDado2() != 5
            and self.__parent.miDado1() + self.__parent.miDado2() != 5
        ):
            return False
        casa = self.__parent.miCasa()
        enCasa = Utils.contarFichas(casa)
        if enCasa == 0:
            return False
        ruta = self.__parent.miRuta()
        f1 = ruta[0][0]
        f2 = ruta[0][1]
        if f1 == None or f2 == None:
            return False
        if self.__parent.esMia(f1) and self.__parent.esMia(f2):
            return False
        for f in self.__parent.miCasa():
            if f != None:
                if self.__parent.intentaSalirDeCasa(f):
                    return True
        return False

    # PRIORIDAD 1: Intentar matar las fichas de los demas.
    def intentaMatarOtraFicha(self):
        # EXCEPCION: Cuando puedes sacar ficha y no tienes con que caminar el bonus.
        if (
            self.__parent.miDado1() == 5
            or self.__parent.miDado2() == 5
            or self.__parent.miDado1() + self.__parent.miDado2() == 5
        ):
            casa = self.__parent.miCasa()
            ruta = self.__parent.miRuta()
            enCasa = Utils.contarFichas(casa)
            enMeta = Utils.contarFichas(ruta[len(ruta) - 1])
            if enCasa == 4 or enCasa + enMeta == 4:
                return False
            if enCasa > 0:
                if 4 - enCasa - enMeta < 2:
                    return False
        for f in self.__parent.misFichas():
            if self.__parent.estaEnCasa(f):
                continue
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
            for mov in movs:
                total = 0
                total += self.__parent.miDado1() if 1 in mov else 0
                total += self.__parent.miDado2() if 2 in mov else 0
                total += self.__parent.miBono1() if 3 in mov else 0
                total += self.__parent.miBono2() if 4 in mov else 0
                if total == 0:
                    continue
                excl = InitStatic.excluir()
                posI = self.__parent.obtenerPosRuta(f)[0]
                for jC in range(len(ruta[posI + total])):
                    fM = ruta[posI + total][jC]
                    if (
                        fM != None
                        and not posI + total in excl
                        and not self.__parent.esMia(fM)
                    ):
                        MoveUtils.moverFichaDirecto(
                            self.__parent,
                            f,
                            mov,
                            self.__parent.miDado1(),
                            self.__parent.miDado2(),
                            self.__parent.miBono1(),
                            self.__parent.miBono2(),
                            self.__parent.miRuta(),
                            excl,
                        )
                        return True
        return False

    # PRIORIDAD 2: Intentar entrar en la meta.
    def intentaEntrarEnMeta(self):
        # EXCEPCION: Cuando puedes sacar ficha y no tienes con que caminar el bonus.
        if (
            self.__parent.miDado1() == 5
            or self.__parent.miDado2() == 5
            or self.__parent.miDado1() + self.__parent.miDado2() == 5
        ):
            casa = self.__parent.miCasa()
            ruta = self.__parent.miRuta()
            enCasa = Utils.contarFichas(casa)
            enMeta = Utils.contarFichas(ruta[len(ruta) - 1])
            if enCasa == 4 or enCasa + enMeta == 4:
                return False
            if enCasa > 0:
                if 4 - enCasa - enMeta < 2:
                    return False
        for f in self.__parent.misFichas():
            if self.__parent.estaEnCasa(f):
                continue
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
            for mov in movs:
                total = 0
                total += self.__parent.miDado1() if 1 in mov else 0
                total += self.__parent.miDado2() if 2 in mov else 0
                total += self.__parent.miBono1() if 3 in mov else 0
                total += self.__parent.miBono2() if 4 in mov else 0
                if total == 0:
                    continue
                ruta = self.__parent.miRuta()
                posI = self.__parent.obtenerPosRuta(f)[0]
                if posI + total == len(ruta) - 1:
                    MoveUtils.moverFichaDirecto(
                        self.__parent,
                        f,
                        mov,
                        self.__parent.miDado1(),
                        self.__parent.miDado2(),
                        self.__parent.miBono1(),
                        self.__parent.miBono2(),
                        self.__parent.miRuta(),
                        InitStatic.excluir(),
                    )
                    return True
        return False

    # PRIORIDAD 3: Sacar fichas de la casa.
    def intentaSacarFicha(self):
        # EXCEPCION: Cuando tienes puente en la salida.
        if (
            self.__parent.miDado1() != 5
            and self.__parent.miDado2() != 5
            and self.__parent.miDado1() + self.__parent.miDado2() != 5
        ):
            return False
        casa = self.__parent.miCasa()
        enCasa = Utils.contarFichas(casa)
        if enCasa == 0:
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
            rowMax = MoveUtils.mayorDistancia(
                movs, self.__parent.miDado1(), self.__parent.miDado2()
            )
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
