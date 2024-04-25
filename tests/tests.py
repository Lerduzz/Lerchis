def bridgets(self, Utils):
    if True:
        roja = self.ui.ficha00
        verde = self.ui.ficha10
        azul = self.ui.ficha20
        self.__turno = 2
        self.salirDeCasa(azul)
        self.__turno = 1
        self.salirDeCasa(verde)
        Utils.moverFicha(self.__rutas[self.__turno],0,0,self.__rutas[self.__turno],14,1)
        self.__turno = 0
        self.salirDeCasa(roja)
        Utils.moverFicha(self.__rutas[self.__turno],0,0,self.__rutas[self.__turno],24,1)
        self.relocateAll()
