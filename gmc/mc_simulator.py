"""Monte Carlo Simulator"""

import networkx as nx
from matplotlib.axes import Axes

from ui.constants import BACKGROUND_COLOR, PRIMARY_COLOR
from gmc.flow_model import FlowModel


class Simulator():
    """MC Simulator Class"""

    def __init__(self, model: FlowModel):
        self._graph = nx.DiGraph()
        self._graph.add_node('origin', name='origin')
        self._graph.add_node('drain', name='drain')
        for source in model.sources:
            self._graph.add_node(source.id, name=source.name)
            if source.time_step > 0:
                self._graph.add_edge('origin', source.id, weight=source.time_step)
        for currency in model.currencies:
            self._graph.add_node(currency.id, name=currency.name)
            if currency.target_value > 0:
                self._graph.add_edge(currency.id, 'drain', weight=currency.target_value)
        for connection in model.connections:
            self._graph.add_edge(connection.source.id, connection.target.id, weight=connection.input_rate/connection.output_rate)

    def draw_flow_graph(self, axes: Axes):
        """Draw flow graph using Matplotlib Axes object"""
        layout = nx.spring_layout(self._graph, weight=None)
        nx.draw_networkx(self._graph, ax=axes, pos=layout, with_labels=False, node_color=PRIMARY_COLOR, edge_color=PRIMARY_COLOR)
        axes.set_facecolor(BACKGROUND_COLOR)
