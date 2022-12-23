"""GMC Model Components"""

from __future__ import annotations

import uuid


class Position():
    """GMC Position Class"""

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Component():
    """GMC Component Class"""

    SIZE = 0.4

    def __init__(self, name: str, position: Position = None):
        self._id = uuid.uuid4()
        self.name = name
        self.pos = position if position is not None else Position()
        self.inputs = []
        self.connections = []

    def add_input(self, connection: Connection):
        """Add input connection to component"""
        if connection.target == self:
            self.inputs.append(connection)

    def add_connection(self, connection: Connection):
        """Add output connection to component"""
        if connection.source == self:
            self.connections.append(connection)

    def delete_connection(self, connection: Connection):
        """Delete input or output connection"""
        if connection in self.inputs:
            self.inputs.remove(connection)
        if connection in self.connections:
            self.connections.remove(connection)

    def to_dict(self):
        """Converts the component into a dictionary"""
        return {'_id': self._id, 'name': self.name, 'pos': (self.pos.x, self.pos.y)}


class Connection():
    """GMC Connection Class"""

    def __init__(self, source: Component, target: Component, input_rate: float = 1, output_rate: float = 1):
        self.source = source
        self.target = target
        self.input_rate = input_rate
        self.output_rate = output_rate
        source.add_connection(self)
        target.add_input(self)

    # pylint: disable=protected-access
    def to_dict(self):
        """Converts the connection into a dictionary"""
        return {'source': self.source._id, 'target': self.target._id, 'output': self.output_rate, 'input': self.input_rate}


class Currency(Component):
    """GMC Currency Class"""

    def __init__(self, name: str, position: Position = None):
        super().__init__(name, position)
        if name == "":
            raise ValueError('Currency name cannot be empty!')


class Origin(Currency):
    """GMC Origin Class"""


class Source(Component):
    """GMC Source Class"""

    SIZE = 0.36

    def __init__(self, name: str, position: Position = None):
        super().__init__(name, position)
        if name == "":
            raise ValueError('Source name cannot be empty!')


class Target(Source):
    """GMC Target Class"""

    def __init__(self, name: str, position: Position = None):
        super().__init__(position)
        if name == "":
            raise ValueError('Target name cannot be empty!')
