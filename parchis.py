import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QResizeEvent
from parchis_ui import Ui_VentanaJuego

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_VentanaJuego() 
        self.ui.setupUi(self)
    
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.ui.cajaTablero.setFixedWidth(self.ui.cajaTablero.height())
        self.ui.dado1.setFixedHeight(self.ui.dado1.width())


app = QApplication([])
application = Ventana()
application.show()
sys.exit(app.exec())