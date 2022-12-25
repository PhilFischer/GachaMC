"""Main Application Controller"""

from PySide2.QtWidgets import QFileDialog

from ui.main_window import MainWindow
from ui.dialogs.currency_dialog import CurrencyDialog
from ui.dialogs.source_dialog import SourceDialog
from ui.dialogs.target_dialog import TargetDialog
from gmc.components import Component, Source, Currency
from gmc.flow_model import FlowModel


class Controller():
    """Controller Class"""

    def __init__(self, main_window: MainWindow):
        self.__connect_source = None
        self.__connect_target = None
        self.model = FlowModel()
        self.model.connect(main_window.canvas.draw_flow_model)

        main_window.menu.add_currency.connect(self.add_currency_event)
        main_window.menu.add_source.connect(self.add_source_event)
        main_window.menu.add_target.connect(self.add_target_event)
        main_window.menu.save_model.connect(self.save_model)
        main_window.menu.load_model.connect(self.load_model)

        self.canvas = main_window.canvas
        self.canvas.connect_selection(self.cavas_selection)
        self.canvas.connect_drag(self.model.move_component_position)

        self.item = main_window.item
        self.item.add_connection.connect(self.add_connection_event)
        self.item.add_input.connect(self.add_input_event)
        self.item.deleted.connect(self.delete_component)
        self.item.connect(self.delete_connection)

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
        dialog = TargetDialog()
        if dialog.exec_():
            target = dialog.target()
            target.pos = self.canvas.center()
            self.model.add_target(target)

    def add_connection_event(self):
        """Resolve add connection event"""
        self.__connect_source = self.canvas.selected_object
        self.__connect_target = None

    def delete_component(self):
        """Resolve delete component event"""
        obj = self.canvas.selected_object
        self.canvas.selected_object = None
        self.model.delete_component(obj)
        self.item.set_item(None)

    def delete_connection(self, connection):
        """Resolve delete connection event"""
        self.model.delete_connection(connection)
        self.item.set_item(self.canvas.selected_object)

    def __complete_connection_event(self, target: Source):
        """Complete connection event"""
        if isinstance(self.__connect_source, Source) and isinstance(target, Currency):
            self.model.add_edge(self.__connect_source, target)
        self.__connect_source = None

    def add_input_event(self):
        """Resolve add input event"""
        self.__connect_target = self.canvas.selected_object
        self.__connect_source = None

    def __complete_input_event(self, source: Currency):
        if isinstance(self.__connect_target, Source) and isinstance(source, Currency):
            self.model.add_edge(source, self.__connect_target)
        self.__connect_target = None

    def cavas_selection(self, component: Component):
        """Resolve canvas selection event"""
        if not self.__connect_source is None:
            self.__complete_connection_event(component)
        elif not self.__connect_target is None:
            self.__complete_input_event(component)
        self.item.set_item(component)

    def save_model(self):
        """Resolve save model event"""
        filename = QFileDialog.getSaveFileName(caption = 'Save Model Graph', dir = 'model.yaml', filter = 'YAML (*.yaml);;All Files (*.*)')
        self.model.save_to_file(filename[0])

    def load_model(self):
        """Resolve load model event"""
        filename = QFileDialog.getOpenFileName(caption = 'Load Model Graph', filter = 'YAML (*.yaml);;All Files (*.*)')
        self.model.load_from_file(filename[0])
