"""Item Panel UI"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QFrame, QPushButton, QDoubleSpinBox

from gmc.components import Component, Connection, Source


class InputWidget(QWidget):
    """Input Widget Class"""

    def __init__(self, connection: Connection):
        super().__init__()
        self.source = connection.source

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(connection.source.name)
        layout.addWidget(title)

        edit = QDoubleSpinBox()
        edit.setValue(1)
        edit.setMinimum(0.01)
        edit.wheelEvent = lambda event: None
        layout.addWidget(edit)


class OutputWidget(QWidget):
    """Output Widget Class"""

    def __init__(self, connection: Connection):
        super().__init__()
        self.target = connection.target

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(connection.target.name)
        layout.addWidget(title)

        edit = QDoubleSpinBox()
        edit.setValue(1)
        edit.setMinimum(0)
        edit.wheelEvent = lambda event: None
        layout.addWidget(edit)


class ItemPanel(QScrollArea):
    """Item Panel Class"""

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(240)
        self.setMaximumWidth(240)
        self.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)

        # Title
        self.__title = QLabel()
        self.__title.setStyleSheet('font-size: 10pt;')
        layout.addWidget(self.__title)

        self.__name = QLabel()
        self.__name.setStyleSheet('font-size: 16pt;')
        layout.addWidget(self.__name)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)
        layout.addSpacing(18)

        # Inputs
        text1 = QLabel("Inputs")
        text1.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text1)

        sources = QWidget()
        self.__sources = QVBoxLayout()
        sources.setLayout(self.__sources)
        layout.addWidget(sources)

        self.__input_button = QPushButton('Add Input')
        self.__input_button.setVisible(False)
        self.add_input = self.__input_button.clicked
        layout.addWidget(self.__input_button)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)
        layout.addSpacing(18)

        # Outputs
        text2 = QLabel("Outputs")
        text2.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text2)

        targets = QWidget()
        self.__targets = QVBoxLayout()
        targets.setLayout(self.__targets)
        layout.addWidget(targets)

        self.__connection_button = QPushButton('Add Output')
        self.__connection_button.setVisible(False)
        self.add_connection = self.__connection_button.clicked
        layout.addWidget(self.__connection_button)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)
        layout.addSpacing(18)


    def set_item(self, item: Component):
        """Set item to be displayed"""
        for i in reversed(range(self.__sources.count())):
            self.__sources.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.__targets.count())):
            self.__targets.itemAt(i).widget().deleteLater()
        if item is None:
            self.__title.setText("")
            self.__name.setText("")
            self.__input_button.setVisible(False)
            self.__connection_button.setVisible(False)
            return
        if isinstance(item, Source):
            self.__input_button.setVisible(True)
            self.__connection_button.setVisible(True)
        else:
            self.__input_button.setVisible(False)
            self.__connection_button.setVisible(False)
        self.__title.setText(str(item.__class__.__name__))
        self.__name.setText(item.name)
        for connection in item.inputs:
            self.__add_source(connection)
        for connection in item.connections:
            self.__add_target(connection)

    def __add_source(self, connection: Connection):
        widget = InputWidget(connection)
        self.__sources.addWidget(widget)

    def __add_target(self, connection: Connection):
        widget = OutputWidget(connection)
        self.__targets.addWidget(widget)
