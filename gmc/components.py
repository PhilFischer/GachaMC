"""GMC Model Components"""

from __future__ import annotations

import uuid
from typing import List


class Position():
    """GMC Position Class"""

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __neg__(self):
        return Position(-self.x, -self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def translate(self, other: Position):
        """Translates the position by the values of other"""
        self.x += other.x
        self.y += other.y


class Component():
    """GMC Component Class"""

    SIZE = 0.4

    def __init__(self, name: str, position: Position = None):
        self.id = uuid.uuid4().hex  # pylint: disable=invalid-name
        self.name: str = name
        self.pos: Position = position if position is not None else Position()
        self.inputs: List[Connection] = []
        self.connections: List[Connection] = []

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
        return {'_id': self.id, 'name': self.name, 'pos': (self.pos.x, self.pos.y)}


class Connection():
    """GMC Connection Class"""

    def __init__(self, source: Component, target: Component, rate: float = 1):
        self.source: Component = source
        self.target: Component = target
        self.rate: float = rate
        source.add_connection(self)
        target.add_input(self)

    # pylint: disable=protected-access
    def to_dict(self):
        """Converts the connection into a dictionary"""
        return {'source': self.source.id, 'target': self.target.id, 'rate': self.rate}


class Currency(Component):
    """GMC Currency Class"""

    def __init__(self, name: str, position: Position = None, target_value: float = 0):
        super().__init__(name, position)
        self.target_value: float = target_value
        if name == "":
            raise ValueError('Currency name cannot be empty!')

    def to_dict(self):
        """Converts the currency into a dictionary"""
        dictionary = super().to_dict()
        dictionary['target_value'] = self.target_value
        return dictionary


class Source(Component):
    """GMC Source Class"""

    SIZE = 0.36

    def __init__(self, name: str, position: Position = None, time_step: float = 1):
        super().__init__(name, position)
        self.time_step: float = time_step
        if name == "":
            raise ValueError('Source name cannot be empty!')

    def to_dict(self):
        """Converts the source into a dictionary"""
        dictionary = super().to_dict()
        dictionary['time_step'] = self.time_step
        return dictionary
