"""Gacha Monte Carlo Application"""

from __future__ import annotations
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication
from qt_material import apply_stylesheet

from controller import Controller
from ui.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication()
    apply_stylesheet(app, theme='dark_lightgreen.xml')

    window = MainWindow()
    controller = Controller(window)
    QTimer.singleShot(0, lambda: Controller.center_window(window))
    window.show()

    app.exec_()
