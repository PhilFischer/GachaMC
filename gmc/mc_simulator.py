"""Monte Carlo Simulator"""

import networkx as nx
from matplotlib.axes import Axes

from ui.constants import BACKGROUND_COLOR, PRIMARY_COLOR
from gmc.flow_model import FlowModel


class Simulator():
    """MC Simulator Class"""

    def __init__(self, model: FlowModel):
        self._graph = nx.DiGraph()
        for comp in model.get_components():
            self._graph.add_node(comp.id, name=comp.name)
        for connection in model.connections:
            self._graph.add_edge(connection.source.id, connection.target.id, weight=connection.output_rate/connection.input_rate)

    def draw_flow_graph(self, axes: Axes):
        """Draw flow graph using Matplotlib Axes object"""
        nx.draw_networkx(self._graph, ax=axes, with_labels=False, node_color=PRIMARY_COLOR)
        axes.set_facecolor(BACKGROUND_COLOR)
