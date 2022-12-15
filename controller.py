"""Main Application Controller"""

from ui.main_window import MainWindow
from ui.dialogs.currency_dialog import CurrencyDialog
from gmc.components import Source, Target
from gmc.flow_model import FlowModel


class Controller():
    """Controller Class"""

    def __init__(self, main_window: MainWindow):
        self.model = FlowModel()
        self.model.connect(main_window.canvas.draw_flow_model)

        main_window.menu.add_currency.connect(self.add_currency_event)
        main_window.menu.add_source.connect(self.add_source_event)
        main_window.menu.add_target.connect(self.add_target_event)

        self.canvas = main_window.canvas
        self.canvas.connect_selection(main_window.item.set_item)
        self.canvas.connect_drag(self.model.move_component_position)

        main_window.canvas.draw_flow_model(self.model)

    def add_currency_event(self):
        """Resolve add currency event"""
        dialog = CurrencyDialog()
        if dialog.exec_():
            currency = dialog.currency()
            currency.pos = self.canvas.center()
            self.model.add_currency(currency)

    def add_source_event(self):
        """Resolve add source event"""
        source = Source(self.canvas.center())
        self.model.add_source(source)

    def add_target_event(self):
        """Resolve add target event"""
        target = Target(self.canvas.center())
        self.model.add_target(target)
