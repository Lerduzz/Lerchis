from PyQt5.QtWidgets import QProxyStyle, QStyle

class EstiloIconos(QProxyStyle):
    def __init__(self, size):
        super().__init__()
        self.__size = size

    def pixelMetric(self, metric, option = 0, widget = 0):
        if metric == QStyle.PM_SmallIconSize:
            return self.__size
        return super().pixelMetric(metric, option, widget)