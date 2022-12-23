"""Menu Panel UI"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame

from ui.constants import PRIMARY_COLOR, SECONDARY_COLOR


class MenuPanel(QWidget):
    """Menu Panel Class"""

    def __init__(self):
        super().__init__()

        self.setMinimumWidth(180)
        self.setMaximumWidth(180)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        currency_button = QPushButton('Add Currency')
        self.add_currency = currency_button.clicked
        layout.addWidget(currency_button)

        source_button = QPushButton('Add Source')
        self.add_source = source_button.clicked
        layout.addWidget(source_button)

        target_button = QPushButton('Add Target')
        target_button.setStyleSheet(f"color: {SECONDARY_COLOR}; border: 2px solid {SECONDARY_COLOR};")
        self.add_target = target_button.clicked
        layout.addWidget(target_button)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"border: 2px solid {PRIMARY_COLOR}; padding: 5px 0px 5px 0px;")
        layout.addWidget(separator)

        save_button = QPushButton('Save Graph')
        save_button.setStyleSheet(f"color: {SECONDARY_COLOR}; border: 2px solid {SECONDARY_COLOR};")
        self.save_model = save_button.clicked
        layout.addWidget(save_button)

        load_button = QPushButton('Load Graph')
        load_button.setStyleSheet(f"color: {SECONDARY_COLOR}; border: 2px solid {SECONDARY_COLOR};")
        self.load_model = load_button.clicked
        layout.addWidget(load_button)
