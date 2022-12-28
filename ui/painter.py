"""Custom painter for flow model objects"""

from __future__ import annotations
from typing import TYPE_CHECKING
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QPixmap, QPen, QBrush

from gmc.components import Position, Connection, Source, Currency
from ui.constants import (PRIMARY_COLOR, PRIMARY_LIGHT_COLOR, PRIMARY_DARK_COLOR,
    SECONDARY_COLOR, SECONDARY_LIGHT_COLOR, SECONDARY_DARK_COLOR)

if TYPE_CHECKING:
    from ui.central_canvas import CentralCanvas


class Painter(QPainter):
    """Extends QPainter to draw flow model components"""

    def __init__(self, pixmap: QPixmap, canvas: CentralCanvas):
        super().__init__(pixmap)
        self.__canvas = canvas

    def drawGridLine(self, pos: Position = None):  # pylint: disable=invalid-name
        """Draws vertical and horizontal grid lines"""
        x, y = self.__canvas.world_to_screen(pos)
        width, height = self.__canvas.pixmap().width(), self.__canvas.pixmap().height()
        self.setPen(QPen(Qt.black, 2))
        self.drawLine(x, 0, x, height)
        self.drawLine(0, y, width, y)

    def drawEdge(self, connection: Connection):  # pylint: disable=invalid-name
        """Draws a line between source and target"""
        x1, y1 = self.__canvas.world_to_screen(connection.source.pos)
        x2, y2 = self.__canvas.world_to_screen(connection.target.pos)
        self.setPen(QPen(Qt.gray, 3))
        self.drawLine(x1, y1, x2, y2)

    def drawCurrency(self, currency: Currency, highlight: bool = False):  # pylint: disable=invalid-name
        """Draws a currency object"""
        x, y = self.__canvas.world_to_screen(currency.pos)
        size = self.__canvas.ppu * Currency.SIZE
        x, y = x - size/2, y - size/2
        self.setPen(QPen(PRIMARY_DARK_COLOR))
        if highlight:
            self.setBrush(QBrush(PRIMARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(PRIMARY_COLOR, Qt.SolidPattern))
        self.drawEllipse(x, y, size, size)
        self.drawText(QRectF(x-2*size, y-size/2-10, 5*size, size), Qt.AlignCenter, currency.name)

    def drawSource(self, source: Source, highlight: bool = False):  # pylint: disable=invalid-name
        """Draws a source object"""
        x, y = self.__canvas.world_to_screen(source.pos)
        size = self.__canvas.ppu * Source.SIZE
        x, y = x - size/2, y - size/2
        self.setPen(QPen(PRIMARY_DARK_COLOR))
        if highlight:
            self.setBrush(QBrush(PRIMARY_LIGHT_COLOR, Qt.SolidPattern))
        else:
            self.setBrush(QBrush(PRIMARY_COLOR, Qt.SolidPattern))
        self.drawRect(x, y, size, size)
        self.drawText(QRectF(x-2*size, y-size/2-10, 5*size, size), Qt.AlignCenter, source.name)
