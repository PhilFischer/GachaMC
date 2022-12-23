"""GMC Flow Model"""

from __future__ import annotations

from typing import List, Callable
import yaml

from gmc.components import Position, Component, Connection, Currency, Origin, Source, Target


class FlowModel():
    """Flow Model Class"""

    def __init__(self):
        self.__callbacks: List[Callable] = []
        self.origin = Origin("Time Step")
        self.currencies: List[Currency] = []
        self.sources: List[Source] = []
        self.targets: List[Target] = []
        self.connections: List[Connection] = []

    def add_currency(self, currency: Currency):
        """Add a currency to the flow model"""
        self.currencies.append(currency)
        for callback in self.__callbacks:
            callback(self)

    def add_source(self, source: Source):
        """Adds a source to the flow model"""
        self.sources.append(source)
        for callback in self.__callbacks:
            callback(self)

    def add_target(self, target: Target):
        """Adds a target to the flow model"""
        self.targets.append(target)
        for callback in self.__callbacks:
            callback(self)

    def add_edge(self, source: Component, target: Component):
        """Adds a connection to the flow model"""
        if isinstance(source, Source) and isinstance(target, Source):
            return
        if isinstance(source, Currency) and isinstance(target, Currency):
            return
        if isinstance(source, Target):
            return
        if isinstance(target, Origin):
            return
        connection = Connection(source, target)
        self.connections.append(connection)
        for callback in self.__callbacks:
            callback(self)

    def move_component_position(self, component: Component, dpos: Position):
        """Sets new position for flow model component"""
        component.pos.x += dpos.x
        component.pos.y += dpos.y
        for callback in self.__callbacks:
            callback(self)

    def delete_component(self, component: Component):
        """Deletes a component from the flow model"""
        for connection in component.inputs[:]:
            self.delete_connection(connection, notify=False)
        for connection in component.connections[:]:
            self.delete_connection(connection, notify=False)
        if isinstance(component, Target):
            self.targets.remove(component)
        elif isinstance(component, Source):
            self.sources.remove(component)
        elif isinstance(component, Currency):
            self.currencies.remove(component)
        for callback in self.__callbacks:
            callback(self)

    def delete_connection(self, connection: Connection, notify: bool = True):
        """Deletes a component from the flow model"""
        connection.source.delete_connection(connection)
        connection.target.delete_connection(connection)
        self.connections.remove(connection)
        if notify:
            for callback in self.__callbacks:
                callback(self)

    def connect(self, callback: Callable):
        """Add a callback for model changes"""
        self.__callbacks.append(callback)

    def save_to_file(self, filename: str):
        """Saves a flow model to a yaml file"""
        model_dict = {
            'origin': self.origin.to_dict(),
            'currencies': [c.to_dict() for c in self.currencies],
            'sources': [s.to_dict() for s in self.sources],
            'targets': [t.to_dict() for t in self.targets],
            'connections': [c.to_dict() for c in self.connections]
        }
        with open(filename, 'w', encoding = 'utf-8') as file:
            file.write(yaml.dump(model_dict))
