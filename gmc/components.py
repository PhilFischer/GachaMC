"""GMC Model Components"""


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

    def __init__(self, position: Position = None):
        self.pos = position if position is not None else Position()


class Currency(Component):
    """GMC Currency Class"""

    def __init__(self, name: str, position: Position = None):
        super().__init__(position)
        self.name = name
        if name == "":
            raise ValueError("Currency name cannot be empty!")


class Origin(Currency):
    """GMC Origin Class"""


class Source(Component):
    """GMC Source Class"""

    SIZE = 0.36


class Target(Source):
    """GMC Target Class"""
