"""Central Canvas UI"""

import math
from typing import Tuple, Callable
from PySide2.QtGui import QPixmap, QMouseEvent, QWheelEvent
from PySide2.QtWidgets import QLabel, QSizePolicy

from gmc.flow_model import FlowModel
from gmc.components import Position, Currency, Origin, Source, Target
from ui.constants import PRIMARY_COLOR, BACKGROUND_COLOR
from ui.painter import Painter


class CentralCanvas(QLabel):
    """Central Canvas Class"""

    def __init__(self):
        super().__init__()

        canvas = QPixmap(720, 580)
        canvas.fill(BACKGROUND_COLOR)
        self.setPixmap(canvas)
        self.setStyleSheet(f"border: 2px solid {PRIMARY_COLOR};")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.ppu = 100
        self.__center = Position()
        self.__selection_callbacks = []
        self.__drag_callbacks = []

        self.__origin = Position(0, 0)
        self.__currencies = []
        self.__sources = []
        self.__targets = []
        self.__drag_start = Position()
        self.__select_obj = None

    def draw_flow_model(self, flow_model: FlowModel) -> None:
        """Draws a flow model"""
        self.__origin = flow_model.origin
        self.__currencies = flow_model.currencies
        self.__sources = flow_model.sources
        self.__targets = flow_model.targets
        self.__redraw()

    def center(self) -> Position:
        """Returns center position"""
        return Position(self.__center.x, self.__center.y)

    def screen_to_world(self, x: int, y: int) -> Position:
        """Maps screen coordinates on the canvas to world coordinates"""
        width, height = self.pixmap().width(), self.pixmap().height()
        return Position((x - width/2)/self.ppu + self.__center.x, (-y + height/2)/self.ppu + self.__center.y)

    def world_to_screen(self, pos: Position) -> Tuple[int, int]:
        """Maps world coordinates to screen coordinates relative to canvas"""
        width, height = self.pixmap().width(), self.pixmap().height()
        return int((pos.x - self.__center.x)*self.ppu + width/2), int(-(pos.y - self.__center.y)*self.ppu + height/2)

    def connect_selection(self, callback: Callable):
        """Add a callback for user selection"""
        self.__selection_callbacks.append(callback)

    def connect_drag(self, callback: Callable):
        """Add a callback for dragging items"""
        self.__drag_callbacks.append(callback)


    def mousePressEvent(self, ev: QMouseEvent):
        pos = self.screen_to_world(ev.pos().x(), ev.pos().y())
        self.__drag_start = pos
        select_obj = None
        for comp in self.__components():
            if abs(pos.x - comp.pos.x) < comp.SIZE/2 and abs(pos.y - comp.pos.y) < comp.SIZE/2:
                select_obj = comp
        self.__select_obj = select_obj
        for callback in self.__selection_callbacks:
            callback(select_obj)
        self.__redraw()
        return super().mouseMoveEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent):
        if self.__select_obj is not None:
            pos = self.screen_to_world(ev.pos().x(), ev.pos().y())
            for callback in self.__drag_callbacks:
                callback(self.__select_obj, Position(pos.x - self.__drag_start.x, pos.y - self.__drag_start.y))
            self.__drag_start = pos
        return super().mouseMoveEvent(ev)

    def wheelEvent(self, ev: QWheelEvent):
        factor = math.exp(ev.delta() / 1000)
        pos = self.screen_to_world(ev.pos().x(), ev.pos().y())
        self.ppu = min(max(self.ppu * factor, 10), 1000)
        dpos = self.screen_to_world(ev.pos().x(), ev.pos().y())
        self.__center = Position(self.__center.x + pos.x - dpos.x, self.__center.y + pos.y - dpos.y)
        self.__redraw()
        return super().wheelEvent(ev)


    def __redraw(self):
        canvas = self.pixmap()
        canvas.fill(BACKGROUND_COLOR)
        painter = Painter(canvas, self)
        painter.drawOrigin(self.__origin.pos)
        for currency in self.__currencies:
            painter.drawCurrency(currency)
        for source in self.__sources:
            painter.drawSource(source)
        for target in self.__targets:
            painter.drawTarget(target)
        if not self.__select_obj is None and isinstance(self.__select_obj, Origin):
            painter.drawOrigin(self.__select_obj.pos, highlight=True)
        elif not self.__select_obj is None and isinstance(self.__select_obj, Currency):
            painter.drawCurrency(self.__select_obj, highlight=True)
        elif not self.__select_obj is None and isinstance(self.__select_obj, Target):
            painter.drawTarget(self.__select_obj, highlight=True)
        elif not self.__select_obj is None and isinstance(self.__select_obj, Source):
            painter.drawSource(self.__select_obj, highlight=True)
        painter.end()
        self.setPixmap(canvas)

    def __components(self):
        return [self.__origin] + self.__currencies + self.__sources + self.__targets
