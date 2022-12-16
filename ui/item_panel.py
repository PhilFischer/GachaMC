"""Item Panel UI"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton

from gmc.components import Component, Connection, Currency, Source, Target


class OutputWidget(QWidget):
    """Output Widget Class"""

    def __init__(self, connection: Connection):
        super().__init__()
        self.target = connection.target


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
        self.__title.setStyleSheet('font-size: 12pt;')
        layout.addWidget(self.__title)

        self.__name = QLabel()
        self.__name.setStyleSheet('font-size: 16pt;')
        layout.addWidget(self.__name)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)
        layout.addSpacing(18)

        text1 = QLabel("Inputs")
        text1.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text1)

        sources = QWidget()
        self.__sources = QVBoxLayout()
        sources.setLayout(self.__sources)
        layout.addWidget(sources)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)
        layout.addSpacing(18)

        text2 = QLabel("Outputs")
        text2.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text2)

        targets = QWidget()
        self.__targets = QVBoxLayout()
        targets.setLayout(self.__targets)
        layout.addWidget(targets)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)
        layout.addSpacing(18)

        self.__connection_button = QPushButton('Add Output')
        self.add_connection = self.__connection_button.clicked
        layout.addWidget(self.__connection_button)


    def set_item(self, item: Component):
        """Set item to be displayed"""
        for i in reversed(range(self.__targets.count())): 
            self.__targets.itemAt(i).widget().deleteLater()       
        if item is None:
            self.__title.setText("")
            self.__name.setText("")
            return
        elif isinstance(item, Target):
            self.__connection_button.isVisible = False
        else:
            self.__connection_button.isVisible = False            
        self.__title.setText(str(item.__class__.__name__))
        for connection in item.connections:
            self.__add_target(connection)
        if isinstance(item, Currency):
            self.__display_currency(item)
        elif isinstance(item, Source):
            self.__display_source(item)

    def __display_currency(self, item: Currency):
        self.__name.setText(item.name)

    def __display_source(self, item: Source):
        pass

    def __add_target(self, connection: Connection):
        name = QLabel(connection.target.name)
        self.__targets.addWidget(name)
