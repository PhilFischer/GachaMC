"""Main Application Controller"""

from ui.main_window import MainWindow
from ui.dialogs.currency_dialog import CurrencyDialog
from ui.dialogs.source_dialog import SourceDialog
from gmc.components import Component, Target
from gmc.flow_model import FlowModel


class Controller():
    """Controller Class"""

    def __init__(self, main_window: MainWindow):
        self.__connect_source = None
        self.model = FlowModel()
        self.model.connect(main_window.canvas.draw_flow_model)

        main_window.menu.add_currency.connect(self.add_currency_event)
        main_window.menu.add_source.connect(self.add_source_event)
        main_window.menu.add_target.connect(self.add_target_event)
        main_window.item.add_connection.connect(self.add_connection_event)

        self.canvas = main_window.canvas
        self.canvas.connect_selection(self.__complete_connection_event)
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
        dialog = SourceDialog()
        if dialog.exec_():
            source = dialog.source()
            source.pos = self.canvas.center()
            self.model.add_source(source)

    def add_target_event(self):
        """Resolve add target event"""
        target = Target(self.canvas.center())
        self.model.add_target(target)

    def add_connection_event(self):
        """Resolve add connection event"""
        self.__connect_source = self.canvas.selected_object

    def __complete_connection_event(self, target: Component):
        """Complete connection event"""
        if self.__connect_source is not None and self.__connect_source != target:
            if target is not None:
                self.model.add_edge(self.__connect_source, target)
            self.__connect_source = None
