from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from parchis_ui import Ui_VentanaJuego


class InitStatic:
    @staticmethod
    def fichas(ui: Ui_VentanaJuego, clicFunc, clicDerFunc) -> list:
        fichas = [
            ui.ficha00,
            ui.ficha01,
            ui.ficha02,
            ui.ficha03,
            ui.ficha10,
            ui.ficha11,
            ui.ficha12,
            ui.ficha13,
            ui.ficha20,
            ui.ficha21,
            ui.ficha22,
            ui.ficha23,
            ui.ficha30,
            ui.ficha31,
            ui.ficha32,
            ui.ficha33,
        ]
        for f in fichas:
            f.clicked.connect(clicFunc)
            f.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            f.customContextMenuRequested.connect(clicDerFunc)
        return fichas

    @staticmethod
    def casas(ui: Ui_VentanaJuego) -> list:
        return [
            [ui.ficha00, ui.ficha01, ui.ficha02, ui.ficha03],
            [ui.ficha10, ui.ficha11, ui.ficha12, ui.ficha13],
            [ui.ficha20, ui.ficha21, ui.ficha22, ui.ficha23],
            [ui.ficha30, ui.ficha31, ui.ficha32, ui.ficha33],
        ]

    @staticmethod
    def caminos() -> list:
        return [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ]

    @staticmethod
    def posCaminos() -> list:
        return [
            (250, 0, 0),
            (250, 50, 0),
            (250, 100, 0),
            (250, 150, 0),
            (250, 200, 0),
            (250, 250, 2),
            (250, 250, 3),
            (250, 250, 4),
            (200, 250, 1),
            (150, 250, 1),
            (100, 250, 1),
            (50, 250, 1),
            (0, 250, 1),
            (0, 400, 1),
            (0, 550, 1),
            (50, 550, 1),
            (100, 550, 1),
            (150, 550, 1),
            (200, 550, 1),
            (250, 700, 5),
            (250, 700, 6),
            (250, 700, 7),
            (250, 700, 0),
            (250, 750, 0),
            (250, 800, 0),
            (250, 850, 0),
            (250, 900, 0),
            (400, 900, 0),
            (550, 900, 0),
            (550, 850, 0),
            (550, 800, 0),
            (550, 750, 0),
            (550, 700, 0),
            (700, 700, 8),
            (700, 700, 9),
            (700, 700, 10),
            (700, 550, 1),
            (750, 550, 1),
            (800, 550, 1),
            (850, 550, 1),
            (900, 550, 1),
            (900, 400, 1),
            (900, 250, 1),
            (850, 250, 1),
            (800, 250, 1),
            (750, 250, 1),
            (700, 250, 1),
            (700, 250, 11),
            (700, 250, 12),
            (700, 250, 13),
            (550, 200, 0),
            (550, 150, 0),
            (550, 100, 0),
            (550, 50, 0),
            (550, 0, 0),
            (400, 0, 0),
        ]

    @staticmethod
    def metas() -> list:
        return [
            [
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None, None, None],
            ],
            [
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None, None, None],
            ],
            [
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None, None, None],
            ],
            [
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None],
                [None, None, None, None],
            ],
        ]

    @staticmethod
    def posMetas() -> list:
        return [
            [
                (400, 50, 0),
                (400, 100, 0),
                (400, 150, 0),
                (400, 200, 0),
                (400, 250, 0),
                (400, 300, 0),
                (475, 400, 14),
            ],
            [
                (50, 400, 1),
                (100, 400, 1),
                (150, 400, 1),
                (200, 400, 1),
                (250, 400, 1),
                (300, 400, 1),
                (400, 475, 15),
            ],
            [
                (400, 850, 0),
                (400, 800, 0),
                (400, 750, 0),
                (400, 700, 0),
                (400, 650, 0),
                (400, 600, 0),
                (475, 550, 16),
            ],
            [
                (850, 400, 1),
                (800, 400, 1),
                (750, 400, 1),
                (700, 400, 1),
                (650, 400, 1),
                (600, 400, 1),
                (550, 475, 17),
            ],
        ]

    @staticmethod
    def rutas(caminos: list, metas: list) -> list:
        result = [[], [], [], []]
        for i in range(3, 56):
            result[0].append(caminos[i])
        for i in range(17, 56):
            result[1].append(caminos[i])
        for i in range(0, 14):
            result[1].append(caminos[i])
        for i in range(31, 56):
            result[2].append(caminos[i])
        for i in range(0, 28):
            result[2].append(caminos[i])
        for i in range(45, 56):
            result[3].append(caminos[i])
        for i in range(0, 42):
            result[3].append(caminos[i])
        for i in range(4):
            result[i] += metas[i]
        return result

    @staticmethod
    def excluir() -> list:
        return [
            0,
            6,
            10,
            14,
            20,
            24,
            28,
            34,
            38,
            42,
            48,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
        ]

    @staticmethod
    def bridges() -> list:
        return [0, 14, 28, 42]

    @staticmethod
    def names() -> list:
        return ["ROJO", "VERDE", "AZUL", "NARANJA"]

    @staticmethod
    def icons() -> list:
        result = [QIcon(), QIcon(), QIcon(), QIcon()]
        result[0].addPixmap(QPixmap(":/rc/images/dados/ficha0.png"), QIcon.Normal, QIcon.Off)
        result[1].addPixmap(QPixmap(":/rc/images/dados/ficha1.png"), QIcon.Normal, QIcon.Off)
        result[2].addPixmap(QPixmap(":/rc/images/dados/ficha2.png"), QIcon.Normal, QIcon.Off)
        result[3].addPixmap(QPixmap(":/rc/images/dados/ficha3.png"), QIcon.Normal, QIcon.Off)
        return result


class AuxStatic:
    @staticmethod
    def iconoMenu(t: int, v: int, s="") -> QIcon:
        icon = QIcon()
        icon.addPixmap(QPixmap(f":/rc/images/dados/dado{t}{s}{v}.png"), QIcon.Normal, QIcon.Off)
        return icon

    @staticmethod
    def fontMenu() -> list:
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        return font
