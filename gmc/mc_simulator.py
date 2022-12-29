"""Monte Carlo Simulator"""

import numpy as np
import networkx as nx
from scipy.optimize import linprog
from matplotlib.axes import Axes

from ui.constants import BACKGROUND_COLOR, PRIMARY_COLOR
from gmc.flow_model import FlowModel


class Simulator():
    """MC Simulator Class"""

    def __init__(self, model: FlowModel):
        self._graph = self._build_networkx_graph(model)
        self._b, inc_inp, inc_out = self._build_flow_matrices(model)
        self._A = inc_inp - inc_out  # pylint: disable=invalid-name
        self._source_rates = None

    @staticmethod
    def _build_flow_matrices(model: FlowModel):
        source_rates = np.zeros(len(model.sources)+1)
        out_incidence = np.zeros((len(model.currencies), len(model.sources)+1))
        inp_incidence = np.zeros((len(model.currencies), len(model.sources)+1))
        cid_lookup = {currency.id: idx for idx, currency in enumerate(model.currencies)}
        for sid, source in enumerate(model.sources):
            source_rates[sid] = 1. / source.time_step if source.time_step > 0 else np.inf
            for connection in source.inputs:
                cid = cid_lookup[connection.source.id]
                out_incidence[cid, sid] = connection.rate
            for connection in source.connections:
                cid = cid_lookup[connection.target.id]
                inp_incidence[cid, sid] = connection.rate
        source_rates[-1] = 1.
        out_incidence[:, -1] = np.array([currency.target_value for currency in model.currencies])
        return source_rates, inp_incidence, out_incidence

    @staticmethod
    def _build_networkx_graph(model: FlowModel):
        graph = nx.DiGraph()
        graph.add_node('drain', name='drain')
        for source in model.sources:
            graph.add_node(source.id, name=source.name)
        for currency in model.currencies:
            graph.add_node(currency.id, name=currency.name)
            if currency.target_value > 0:
                graph.add_edge(currency.id, 'drain')
        for connection in model.connections:
            graph.add_edge(connection.source.id, connection.target.id, capacity=connection.rate)
        return graph

    def compute_max_flow(self):
        """Finds maximum model flow using linear programming"""
        nc, ns = self._A.shape
        target = np.zeros(ns)
        target[-1] = 1.
        bounds = np.stack([np.zeros(ns), self._b], axis=1)
        result = linprog(-target, -self._A, np.zeros(nc), bounds=bounds)
        result = linprog(np.ones(ns), -self._A, np.zeros(nc), target.reshape((1, -1)), result.x[-1], bounds=bounds)
        ret = {'status': result.status, 'message': result.message}
        if result.status == 0:
            ret['steps'] = 1. / result.x[-1] if result.x[-1] > 0 else 0.
            ret['s'] = result.x[:-1]
            ret['c'] = np.matmul(self._A, result.x)
            self._source_rates = result.x[:-1]
        return ret

    def draw_flow_graph(self, axes: Axes):
        """Draw flow graph using Matplotlib Axes object"""
        layout = nx.fruchterman_reingold_layout(self._graph, iterations=500)
        nx.draw_networkx(self._graph, ax=axes, pos=layout, node_color=PRIMARY_COLOR, edge_color=PRIMARY_COLOR, with_labels=False)
        axes.set_facecolor(BACKGROUND_COLOR)
