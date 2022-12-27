"""Monte Carlo Simulator"""

import networkx as nx
from matplotlib.axes import Axes

from ui.constants import BACKGROUND_COLOR, PRIMARY_COLOR
from gmc.flow_model import FlowModel


class Simulator():
    """MC Simulator Class"""

    def __init__(self, model: FlowModel):
        self._origin = model.origin.id
        self._graph = nx.DiGraph()
        for comp in model.get_components():
            self._graph.add_node(comp.id, name=comp.name)
        for connection in model.connections:
            self._graph.add_edge(connection.source.id, connection.target.id, weight=connection.input_rate/connection.output_rate)

    def draw_flow_graph(self, axes: Axes):
        """Draw flow graph using Matplotlib Axes object"""
        layout = nx.spring_layout(self._graph, weight=None)
        nx.draw_networkx(self._graph, ax=axes, pos=layout, with_labels=False, node_color=PRIMARY_COLOR, edge_color=PRIMARY_COLOR)
        axes.set_facecolor(BACKGROUND_COLOR)
