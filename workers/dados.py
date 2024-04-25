import time, random
from PyQt5.QtCore import QObject, pyqtSignal

class DadosWorker(QObject):
    finished = pyqtSignal(int, int)
    progress = pyqtSignal(int, int)

    def __init__(self, s1, s2):
        super().__init__()
        self.__s1 = s1
        self.__s2 = s2
        self.__r1 = random.randint(1, 6)
        self.__r2 = random.randint(1, 6)

    def run(self):
        d1C = 0
        d2C = 0
        alt = random.randint(1, 6)
        flag = 0
        skip = random.randint(1, 2)
        m1 = random.randint(2, 4)
        m2 = random.randint(2, 4)
        while d1C < m1 or d2C < m2:
            if alt <= 3:
                if flag >= skip:
                    d1C += 1 if d1C < m1 and self.__s1 == self.__r1 else 0
                    self.__s1 += 1 if d1C < m1 else 0
                    self.__s1 = 1 if self.__s1 > 6 else self.__s1
                    flag = 0
                else:
                    flag += 1
            else:
                d1C += 1 if d1C < m1 and self.__s1 == self.__r1 else 0
                self.__s1 += 1 if d1C < m1 else 0
                self.__s1 = 1 if self.__s1 > 6 else self.__s1
            if alt >= 4:
                if flag >= skip:
                    d2C += 1 if d2C < m2 and self.__s2 == self.__r2 else 0
                    self.__s2 += 1 if d2C < m2 else 0
                    self.__s2 = 1 if self.__s2 > 6 else self.__s2
                    flag = 0
                else:
                    flag += 1
            else:
                d2C += 1 if d2C < m2 and self.__s2 == self.__r2 else 0
                self.__s2 += 1 if d2C < m2 else 0
                self.__s2 = 1 if self.__s2 > 6 else self.__s2
            self.progress.emit(self.__s1, self.__s2)
            time.sleep(0.01)
        self.finished.emit(self.__r1, self.__r2)