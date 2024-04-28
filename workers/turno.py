import time
from PyQt5.QtCore import QObject, pyqtSignal


class TurnoWorker(QObject):
    started = pyqtSignal(int)
    finished = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, start):
        super().__init__()
        self.__max = start * 10
        self.__value = 0
        self.__interval = 0.1

    def run(self):
        try:
            self.started.emit(self.__max // 10)
            while self.__value < self.__max:
                self.progress.emit(self.__value // 10)
                self.__value += 1
                time.sleep(self.__interval)
            self.finished.emit(self.__value // 10)
        except RuntimeError:
            pass

    def faster(self):
        self.__interval = 0.0025

    def isFast(self) -> float:
        return self.__interval == 0.0025
