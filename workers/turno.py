import time
from PyQt5.QtCore import QObject, pyqtSignal

class TurnoWorker(QObject):
    started = pyqtSignal(int)
    finished = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, start):
        super().__init__()
        self.__max = start
        self.__value = 0
        self.__interval = 0.9

    def run(self):
        self.started.emit(self.__max)
        while self.__value < self.__max:
            self.progress.emit(self.__value)
            self.__value += 1
            time.sleep(self.__interval)
        self.finished.emit(self.__value)

    def faster(self):
        self.__interval = 0.025
