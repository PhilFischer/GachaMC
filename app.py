"""Gacha Monte Carlo Application"""

from __future__ import annotations
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QApplication, QStyle
from qt_material import apply_stylesheet

from controller import Controller
from ui.main_window import MainWindow


def center_window(widget):
    """Centers the application window"""
    widget_window = widget.window()
    widget_window.setGeometry(
        QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            window.size(),
            QGuiApplication.primaryScreen().availableGeometry(),
        )
    )

if __name__ == '__main__':
    app = QApplication()
    apply_stylesheet(app, theme='dark_lightgreen.xml')

    window = MainWindow()
    controller = Controller(window)
    QTimer.singleShot(0, lambda: center_window(window))
    window.show()

    app.exec_()
