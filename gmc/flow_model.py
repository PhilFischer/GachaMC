"""GMC Flow Model"""

from __future__ import annotations

from typing import List, Callable
import yaml

from gmc.components import Position, Component, Connection, Currency, Source


class FlowModel():
    """Flow Model Class"""

    def __init__(self):
        self.__callbacks: List[Callable] = []
        self.currencies: List[Currency] = []
        self.sources: List[Source] = []
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

    def add_edge(self, source: Component, target: Component):
        """Adds a default connection to the flow model"""
        if isinstance(source, Source) and isinstance(target, Source):
            return
        if isinstance(source, Currency) and isinstance(target, Currency):
            return
        connection = Connection(source, target)
        self.connections.append(connection)
        for callback in self.__callbacks:
            callback(self)

    def add_connection(self, connection: Connection):
        """Adds a connection to the flow model"""
        self.connections.append(connection)
        for callback in self.__callbacks:
            callback(self)

    def get_components(self) -> List[Component]:
        """Returns list of all components"""
        return self.currencies + self.sources

    def num_components(self) -> int:
        """Returns the number of components"""
        return len(self.get_components())

    def move_component_position(self, component: Component, dpos: Position):
        """Sets new position for flow model component"""
        component.pos.translate(dpos)
        for callback in self.__callbacks:
            callback(self)

    def delete_component(self, component: Component):
        """Deletes a component from the flow model"""
        for connection in component.inputs[:]:
            self.delete_connection(connection, notify=False)
        for connection in component.connections[:]:
            self.delete_connection(connection, notify=False)
        if isinstance(component, Source):
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

    def layout(self):
        """Return node layout as dictionary"""
        return {comp.id: comp.pos.coords() for comp in self.get_components()}

    def avg_connection_length(self):
        """Return average node distance"""
        return sum(conn.length() for conn in self.connections) / len(self.connections)

    def normalize_positions(self):
        """Shift component positions such that the first component has position (0,0)"""
        dpos = self.get_components()[0].pos
        for component in reversed(self.get_components()):
            self.move_component_position(component, -dpos)

    def connect(self, callback: Callable):
        """Add a callback for model changes"""
        self.__callbacks.append(callback)

    def copy(self):
        """Return copy of this flow model"""
        other = FlowModel()
        for source in self.sources:
            other_source = Source(source.name, source.pos, time_step=source.time_step)
            other.add_source(other_source)
        for currency in self.currencies:
            other_currency = Currency(currency.name, currency.pos, target_value=currency.target_value)
            other.add_currency(other_currency)
        for connection in self.connections:
            sid = self.get_components().index(connection.source)
            tid = self.get_components().index(connection.target)
            other_connection = Connection(other.get_components()[sid], other.get_components()[tid], rate=connection.rate)
            other.add_connection(other_connection)
        return other

    def save_to_file(self, filename: str):
        """Saves a flow model to a yaml file"""
        model_dict = {
            'currencies': [c.to_dict() for c in self.currencies],
            'sources': [s.to_dict() for s in self.sources],
            'connections': [c.to_dict() for c in self.connections]
        }
        with open(filename, 'w', encoding = 'utf-8') as file:
            yaml.dump(model_dict, file)

    def load_from_file(self, filename: str):
        """Loads the flow model from a yaml file"""
        model_dict = {}
        with open(filename, 'r', encoding = 'utf-8') as file:
            model_dict = yaml.load(file, yaml.FullLoader)
        if 'currencies' in model_dict:
            self.currencies = []
            for data in model_dict['currencies']:
                try:
                    currency = Currency(data['name'], Position(data['pos'][0], data['pos'][1]), target_value=data['target_value'])
                    currency.id = data['_id']
                    self.add_currency(currency)
                except (KeyError, IndexError) as exc:
                    raise RuntimeError('Error loading currency. Malformed yaml file.') from exc
        if 'sources' in model_dict:
            self.sources = []
            for data in model_dict['sources']:
                try:
                    source = Source(data['name'], Position(data['pos'][0], data['pos'][1]), time_step=data['time_step'])
                    source.id = data['_id']
                    self.add_source(source)
                except (KeyError, IndexError) as exc:
                    raise RuntimeError('Error loading source. Malformed yaml file.') from exc
        if 'connections' in model_dict:
            self.connections = []
            for data in model_dict['connections']:
                try:
                    source = next(s for s in self.get_components() if s.id == data['source'])
                    target = next(t for t in self.get_components() if t.id == data['target'])
                    connection = Connection(source, target, rate=data['rate'])
                    self.add_connection(connection)
                except (KeyError, IndexError) as exc:
                    raise RuntimeError('Error loading connection. Malformed yaml file.') from exc
        for callback in self.__callbacks:
            callback(self)
