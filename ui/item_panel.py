"""Item Panel UI"""

from PySide2.QtCore import Qt, QSize, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QToolButton, QDoubleSpinBox

from ui.constants import DANGER_COLOR
from gmc.components import Component, Connection, Source, Currency


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
        edit.setMinimum(0.01)
        edit.setMaximum(10000)
        edit.setValue(connection.rate)
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
        self.connection.rate = value


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
        edit.setMinimum(0.01)
        edit.setMaximum(10000)
        edit.setValue(connection.rate)
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
        self.connection.rate = value


class SourcePanel(QWidget):
    """Source Panel Class"""

    connection_deleted = Signal(Connection)

    def __init__(self, source: Source):
        super().__init__()
        self.source = source

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel('Source Node')
        title.setStyleSheet('font-size: 10pt;')
        layout.addWidget(title)

        name = QLabel(source.name)
        name.setStyleSheet('font-size: 16pt;')
        layout.addWidget(name)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)
        layout.addSpacing(18)

        time_label = QLabel('Time Step')
        layout.addWidget(time_label)

        edit = QDoubleSpinBox()
        edit.setMinimum(0)
        edit.setMaximum(1000)
        edit.setValue(source.time_step)
        edit.wheelEvent = lambda event: None
        edit.valueChanged.connect(self.change_value)
        layout.addWidget(edit)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)
        layout.addSpacing(18)

        text1 = QLabel("Inputs")
        text1.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text1)

        for connection in source.inputs:
            widget = InputWidget(connection)
            widget.deleted.connect(self._notify_connection_deleted(connection))
            layout.addWidget(widget)

        input_button = QPushButton('Add Input')
        self.add_input = input_button.clicked
        layout.addWidget(input_button)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)
        layout.addSpacing(18)

        text2 = QLabel("Outputs")
        text2.setStyleSheet('font-size: 12pt;')
        layout.addWidget(text2)

        for connection in source.connections:
            widget = OutputWidget(connection)
            widget.deleted.connect(self._notify_connection_deleted(connection))
            layout.addWidget(widget)

        connection_button = QPushButton('Add Output')
        self.add_connection = connection_button.clicked
        layout.addWidget(connection_button)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)
        layout.addSpacing(18)

        delete_button = QPushButton('Delete')
        delete_button.setStyleSheet(f"color: {DANGER_COLOR}; border: 2px solid {DANGER_COLOR};")
        self.deleted = delete_button.clicked
        layout.addWidget(delete_button)

    def change_value(self, value):
        """Resolve change time step value event"""
        self.source.time_step = value

    def _notify_connection_deleted(self, connection: Connection):
        return lambda: self.connection_deleted.emit(connection)


class CurrencyPanel(QWidget):
    """Curency Panel Class"""

    def __init__(self, currency: Currency):
        super().__init__()
        self.currency = currency

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel('Currency Node')
        title.setStyleSheet('font-size: 10pt;')
        layout.addWidget(title)

        name = QLabel(currency.name)
        name.setStyleSheet('font-size: 16pt;')
        layout.addWidget(name)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)
        layout.addSpacing(18)

        target_label = QLabel('Target Value')
        layout.addWidget(target_label)

        edit = QDoubleSpinBox()
        edit.setMinimum(0)
        edit.setMaximum(1000000)
        edit.setValue(currency.target_value)
        edit.wheelEvent = lambda event: None
        edit.valueChanged.connect(self.change_value)
        layout.addWidget(edit)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)
        layout.addSpacing(18)

        delete_button = QPushButton('Delete')
        delete_button.setStyleSheet(f"color: {DANGER_COLOR}; border: 2px solid {DANGER_COLOR};")
        self.deleted = delete_button.clicked
        layout.addWidget(delete_button)

    def change_value(self, value):
        """Resolve change target value event"""
        self.currency.target_value = value


class ItemPanel(QScrollArea):
    """Item Panel Class"""

    updated = Signal(Connection)
    deleted = Signal()
    add_input = Signal()
    add_connection = Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(240)
        self.setMaximumWidth(240)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QVBoxLayout()
        self.content.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(self.content)
        self.setWidget(widget)

    def set_item(self, item: Component):
        """Set item to be displayed"""
        prev = self.content.takeAt(0)
        if prev is not None:
            prev.widget().deleteLater()

        if isinstance(item, Currency):
            panel = CurrencyPanel(item)
            panel.deleted.connect(self.deleted.emit)
            self.content.addWidget(panel)
        elif isinstance(item, Source):
            panel = SourcePanel(item)
            panel.connection_deleted.connect(self.updated.emit)
            panel.deleted.connect(self.deleted.emit)
            panel.add_input.connect(self.add_input.emit)
            panel.add_connection.connect(self.add_connection.emit)
            self.content.addWidget(panel)
