"""Monte Carlo Simulator"""

import numpy as np
import networkx as nx
from scipy.optimize import linprog

from gmc.flow_model import FlowModel


class Simulator():
    """MC Simulator Class"""

    def __init__(self, model: FlowModel):
        self.step_num = 0
        self.status = 0
        self._model = model.copy()
        self._graph = self._build_networkx_graph(self._model)
        rates, inc_inp, inc_out = self._build_flow_matrices(self._model)
        self._flow_info = self._compute_max_flow(inc_inp-inc_out, rates)
        if self._flow_info['status'] == 0:
            for idx, source in enumerate(self._model.sources):
                if self._flow_info['s'][idx] == 0:
                    self.status = 2
                source.prop = {
                    'name': source.name,
                    'opt_time': 1./self._flow_info['s'][idx] if self._flow_info['s'][idx] > 0 else 0,
                    'min_time': source.time_step,
                    'steps': 0
                }
            for idx, currency in enumerate(self._model.currencies):
                currency.prop = {
                    'name': currency.name,
                    'delta': self._flow_info['c'][idx],
                    'target': currency.target_value,
                    'storage': 0,
                    'p_storage': 0
                }
        else:
            self.status = 1

    @staticmethod
    def _build_flow_matrices(model: FlowModel):
        source_rates = np.zeros(len(model.sources)+1)
        out_incidence = np.zeros((len(model.currencies), len(model.sources)+1))
        inp_incidence = np.zeros((len(model.currencies), len(model.sources)+1))
        cid_lookup = {currency.id: idx for idx, currency in enumerate(model.currencies)}
        for sid, source in enumerate(model.sources):
            source_rates[sid] = 1./source.time_step if source.time_step > 0 else np.inf
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

    @staticmethod
    def _compute_max_flow(A: np.ndarray, b: np.ndarray):
        """Finds maximum model flow using linear programming with positive contstraints A and upper bounds b"""
        nc, ns = A.shape
        target = np.zeros(ns)
        target[-1] = 1.
        bounds = np.stack([np.zeros(ns), b], axis=1)
        result = linprog(-target, -A, np.zeros(nc), bounds=bounds)
        result = linprog(np.ones(ns), -A, np.zeros(nc), target.reshape((1, -1)), result.x[-1], bounds=bounds)
        ret = {'status': result.status, 'message': result.message}
        if result.status == 0:
            ret['steps'] = 1. / result.x[-1] if result.x[-1] > 0 else 0.
            ret['s'] = result.x[:-1]
            ret['c'] = np.matmul(A, result.x)
        return ret

    def flow_info(self):
        """Return flow info"""
        return self._flow_info

    def graph(self):
        """Return networkx graph"""
        return self._graph

    def layout(self):
        """Return model node layout as dictionary"""
        return nx.spring_layout(self._graph, pos=self._model.layout(), fixed=self._model.layout().keys(),
            k=self._model.avg_connection_length()/self._model.num_components()/8, iterations=500)

    def stage(self):
        """Returns number of stages completed
        (Currently only a single stage is supported)
        """
        return int(all(curr.prop['storage'] >= curr.target_value for curr in self._model.currencies))

    def source_properties(self):
        """Returns current source properties"""
        return {source.id: source.prop for source in self._model.sources}

    def currency_properties(self):
        """Returns current currency storage"""
        return {curr.id: curr.prop for curr in self._model.currencies}

    def step(self):
        """Performs one simulation time step"""
        self.step_num += 1
        for currency in self._model.currencies:
            currency.prop['p_storage'] = currency.prop['storage']
        for source in self._model.sources:
            if source.prop['steps'] < 0:
                source.prop['steps'] += 1
                continue
            if any(conn.source.prop['p_storage'] < conn.rate for conn in source.inputs):
                source.prop['steps'] += 1
                continue
            source.prop['steps'] = source.prop['steps'] - source.prop['opt_time'] + 1
            for conn in source.inputs:
                conn.source.prop['storage'] = conn.source.prop['storage'] - conn.rate
            for conn in source.connections:
                conn.target.prop['storage'] = conn.target.prop['storage'] + conn.rate
