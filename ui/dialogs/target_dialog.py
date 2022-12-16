"""Target Dialog UI"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit

from gmc.flow_model import Target


class TargetDialog(QDialog):
    """Target Dialog Class"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Target")
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumWidth(280)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_edit = QLineEdit("Name")
        layout.addWidget(self.name_edit)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def target(self):
        """Build target from inputs"""
        if self.name_edit.text() == "":
            return None
        return Target(self.name_edit.text())
