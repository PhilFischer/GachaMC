"""Custom painter for flow model objects"""

from typing import Any
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QPixmap, QPen, QBrush

from gmc.components import Position, Source, Currency, Target
from ui.constants import PRIMARY_COLOR, PRIMARY_LIGHT_COLOR, SECONDARY_COLOR, SECONDARY_LIGHT_COLOR


class Painter(QPainter):
    """Extends QPainter to draw flow model components"""

    def __init__(self, pixmap: QPixmap, canvas: Any):
        super().__init__(pixmap)
        self.__canvas = canvas

    def drawGridLine(self, pos: Position = None):  # pylint: disable=invalid-name
        """Draws vertical and horizontal grid lines"""
        x, y = self.__canvas.world_to_screen(pos)
        width, height = self.__canvas.pixmap().width(), self.__canvas.pixmap().height()
        self.setPen(QPen(Qt.black, 2))
        self.drawLine(x, 0, x, height)
        self.drawLine(0, y, width, y)

    def drawCurrency(self, currency: Currency, highlight: bool = False):  # pylint: disable=invalid-name
        """Draws a currency object"""
        x, y = self.__canvas.world_to_screen(currency.pos)
        size = self.__canvas.ppu * Currency.SIZE - 6
        x, y = x + 3 - size/2, y + 3 - size/2
        if highlight:
            self.setBrush(QBrush(PRIMARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(PRIMARY_COLOR, Qt.SolidPattern))
        self.drawEllipse(x, y, size, size)

    def drawSource(self, source: Source, highlight: bool = False):  # pylint: disable=invalid-name
        """Draws a source object"""
        x, y = self.__canvas.world_to_screen(source.pos)
        size = self.__canvas.ppu * Source.SIZE
        x, y = x - size/2, y - size/2
        if highlight:
            self.setBrush(QBrush(PRIMARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(PRIMARY_COLOR, Qt.SolidPattern))
        self.drawRect(x, y, size, size)

    def drawOrigin(self, position: Position = Position(0, 0), highlight: bool = False):  # pylint: disable=invalid-name
        """Draws origin object"""
        x, y = self.__canvas.world_to_screen(position)
        size = self.__canvas.ppu * Currency.SIZE - 6
        x, y = x + 3 - size/2, y + 3 - size/2
        if highlight:
            self.setBrush(QBrush(SECONDARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(SECONDARY_COLOR, Qt.SolidPattern))
        self.drawEllipse(x, y, size, size)

    def drawTarget(self, target: Target, highlight: bool = False):  # pylint: disable=invalid-name
        """Draws target object"""
        x, y = self.__canvas.world_to_screen(target.pos)
        size = self.__canvas.ppu * Source.SIZE
        x, y = x - size/2, y - size/2
        if highlight:
            self.setBrush(QBrush(SECONDARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(SECONDARY_COLOR, Qt.SolidPattern))
        self.drawRect(x, y, size, size)
