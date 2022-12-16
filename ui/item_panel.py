"""Item Panel UI"""

from typing import Callable
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QToolButton, QDoubleSpinBox

from ui.constants import DANGER_COLOR
from gmc.components import Component, Connection, Origin, Source


class InputWidget(QWidget):
    """Input Widget Class"""

    def __init__(self, connection: Connection):
        super().__init__()
        self.connection = connection

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(connection.source.name)
        layout.addWidget(title)

        controls = QHBoxLayout()
        control_widget = QWidget()
        control_widget.setLayout(controls)
        layout.addWidget(control_widget)

        edit = QDoubleSpinBox()
        edit.setValue(connection.output_rate)
        edit.setMinimum(0.01)
        edit.setMaximum(10000)
        edit.wheelEvent = lambda event: None
        edit.valueChanged.connect(self.change_value)
        controls.addWidget(edit)

        delete_button = QToolButton()
        delete_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        delete_button.setIcon(QIcon('img/xmark-solid.png'))
        delete_button.setIconSize(QSize(18, 18))
        self.deleted = delete_button.clicked
        controls.addWidget(delete_button)

    def change_value(self, value):
        """Resolve change value event"""
        self.connection.output_rate = value


class OutputWidget(QWidget):
    """Output Widget Class"""

    def __init__(self, connection: Connection):
        super().__init__()
        self.connection = connection

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(connection.target.name)
        layout.addWidget(title)

        controls = QHBoxLayout()
        control_widget = QWidget()
        control_widget.setLayout(controls)
        layout.addWidget(control_widget)

        edit = QDoubleSpinBox()
        edit.setValue(connection.input_rate)
        edit.setMinimum(0.01)
        edit.setMaximum(10000)
        edit.wheelEvent = lambda event: None
        edit.valueChanged.connect(self.change_value)
        controls.addWidget(edit)

        delete_button = QToolButton()
        delete_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        delete_button.setIcon(QIcon('img/xmark-solid.png'))
        delete_button.setIconSize(QSize(18, 18))
        self.deleted = delete_button.clicked
        controls.addWidget(delete_button)

    def change_value(self, value):
        """Resolve change value event"""
        self.connection.input_rate = value


class ItemPanel(QScrollArea):
    """Item Panel Class"""

    def __init__(self):
        super().__init__()
        self.__callbacks = []

        self.setMinimumWidth(240)
        self.setMaximumWidth(240)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

        self.__delete_button = QPushButton('Delete')
        self.__delete_button.setStyleSheet(f"color: {DANGER_COLOR}; border: 2px solid {DANGER_COLOR};")
        self.__delete_button.setVisible(False)
        self.deleted = self.__delete_button.clicked
        layout.addWidget(self.__delete_button)


    def set_item(self, item: Component):
        """Set item to be displayed"""
        for i in reversed(range(self.__sources.count())):
            self.__sources.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.__targets.count())):
            self.__targets.itemAt(i).widget().deleteLater()
        if isinstance(item, Source):
            self.__input_button.setVisible(True)
            self.__connection_button.setVisible(True)
        else:
            self.__input_button.setVisible(False)
            self.__connection_button.setVisible(False)
        if isinstance(item, Component) and not isinstance(item, Origin):
            self.__delete_button.setVisible(True)
        else:
            self.__delete_button.setVisible(False)
        if item is None:
            self.__title.setText("")
            self.__name.setText("")
            return
        self.__title.setText(str(item.__class__.__name__))
        self.__name.setText(item.name)
        for connection in item.inputs:
            self.__add_source(connection)
        for connection in item.connections:
            self.__add_target(connection)

    def connect(self, callback: Callable):
        """Add callback for deleted connections"""
        self.__callbacks.append(callback)

    def delete_connection(self, connection):
        """Resolve delete connection event"""
        for callback in self.__callbacks:
            callback(connection)

    def __add_source(self, connection: Connection):
        widget = InputWidget(connection)
        widget.deleted.connect(lambda: self.delete_connection(connection))
        self.__sources.addWidget(widget)

    def __add_target(self, connection: Connection):
        widget = OutputWidget(connection)
        widget.deleted.connect(lambda: self.delete_connection(connection))
        self.__targets.addWidget(widget)
