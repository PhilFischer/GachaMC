"""Item Panel UI"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel

from gmc.components import Component


class ItemPanel(QWidget):
    """Item Panel Class"""

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(240)
        self.setMaximumWidth(240)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.__title = QLabel()
        layout.addWidget(self.__title)

    def set_item(self, item: Component):
        """Set item to be displayed"""
        self.__title.setText(str(item.__class__.__name__))
