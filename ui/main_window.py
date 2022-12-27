"""Main Window UI"""

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy

from ui.menu_panel import MenuPanel
from ui.central_canvas import CentralCanvas
from ui.item_panel import ItemPanel


class MainWindow(QMainWindow):
    """Main Window Class"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gacha Monte Carlo')
        self.setWindowIcon(QIcon('img/gmc-logo.png'))

        layout = QHBoxLayout()

        # West Panel: General Menu
        self.menu = MenuPanel()
        layout.addWidget(self.menu)

        # Center Panel: Canvas and Buttons
        center = QVBoxLayout()
        self.canvas = CentralCanvas()
        center.addWidget(self.canvas)

        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignCenter)
        play_button = QPushButton()
        play_button.setMinimumWidth(112)
        play_button.setIcon(QIcon('img/play-solid.png'))
        play_button.setIconSize(QSize(26, 26))
        self.start_simulation = play_button.clicked
        buttons.addWidget(play_button)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons)
        buttons_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        center.addWidget(buttons_widget)

        center_widget = QWidget()
        center_widget.setLayout(center)
        layout.addWidget(center_widget)

        # East Panel: Detail Info
        self.item = ItemPanel()
        layout.addWidget(self.item)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
