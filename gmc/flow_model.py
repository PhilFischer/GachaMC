"""GMC Flow Model"""

from typing import List, Callable

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
        connection = Connection(source, target)
        if isinstance(connection.source, Target):
            return
        if isinstance(connection.target, Origin):
            return
        self.connections.append(connection)
        for callback in self.__callbacks:
            callback(self)

    def move_component_position(self, component: Component, dpos: Position):
        """Sets new position for flow model component"""
        component.pos.x += dpos.x
        component.pos.y += dpos.y
        for callback in self.__callbacks:
            callback(self)

    def connect(self, callback: Callable):
        """Add a callback for model changes"""
        self.__callbacks.append(callback)
