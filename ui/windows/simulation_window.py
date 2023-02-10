"""Simulation Window UI"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from networkx import draw_networkx, draw_networkx_nodes
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSizePolicy

from ui.constants import PRIMARY_COLOR, BACKGROUND_COLOR
from gmc.flow_model import FlowModel
from gmc.mc_simulator import Simulator

matplotlib.use('Qt5Agg')
plt.style.use('dark_background')


class MplCanvas(FigureCanvasQTAgg):
    """Matplotlib Canvas Class"""

    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=BACKGROUND_COLOR)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class SimulationWindow(QWidget):
    """Simulation Window Class"""

    def __init__(self, model: FlowModel):
        super().__init__(parent=None)
        self.simulator = Simulator(model)
        self.currency_names = {curr_id: prop['name'] for curr_id, prop in self.simulator.currency_properties().items()}
        self.__selected_currency = None

        # Simulation
        self.currency_storage = {curr_id: [0] for curr_id in self.simulator.currency_properties()}
        while self.simulator.stage() < 1:
            self.simulator.step()
            for curr_id, properties in self.simulator.currency_properties().items():
                self.currency_storage[curr_id].append(properties['storage'])

        # UI
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Currency Flow Simulation")

        # UI Title
        title = QLabel("Currency Flow Simulation")
        title.setStyleSheet('font-size: 24pt; padding: 30px;')
        layout.addWidget(title)

        # UI Model Info
        center = QHBoxLayout()

        info = QVBoxLayout()
        flow = self.simulator.flow_info()
        if flow['status'] == 0:
            status_panel = QLabel(flow['message'])
            status_panel.setWordWrap(True)
            status_panel.setStyleSheet('background-color: green; padding: 8px 5px 8px 5px; margin: 10px;')
            info.addWidget(status_panel)
            max_panel = QLabel(f"Simulated Time: {self.simulator.step_num} time steps")
            max_panel.setStyleSheet('font-size: 12pt; margin: 0px 10px 0px 10px;')
            info.addWidget(max_panel)
            opt_panel = QLabel(f"Throughput Time: {flow['steps']} time steps")
            opt_panel.setStyleSheet('font-size: 12pt; margin: 0px 10px 0px 10px;')
            info.addWidget(opt_panel)
        else:
            status_panel = QLabel(flow['message'])
            status_panel.setWordWrap(True)
            status_panel.setStyleSheet('background-color: green; padding: 8px 5px 8px 5px;')
            info.addWidget(status_panel)
        info.addSpacing(10)
        currency_label = QLabel('Currency')
        currency_label.setStyleSheet('font-size: 10pt;')
        info.addWidget(currency_label)
        currency_selector = QComboBox()
        currency_selector.addItem('All')
        currency_selector.addItems(self.currency_names.values())
        currency_selector.currentIndexChanged.connect(self._select_currency)
        info.addWidget(currency_selector)
        info.addStretch()
        info_widget = QWidget()
        info_widget.setLayout(info)
        center.addWidget(info_widget)

        self.graph_plot = MplCanvas(width=3, height=3)
        center.addWidget(self.graph_plot)

        center_widget = QWidget()
        center_widget.setLayout(center)
        layout.addWidget(center_widget)

        # UI Currencies
        self.currency_plot = MplCanvas()
        self.currency_plot.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        layout.addWidget(self.currency_plot)

        # Draw
        self._draw_plots()

    def _select_currency(self, index):
        if index == 0:
            self.__selected_currency = None
        else:
            self.__selected_currency = list(self.currency_names.keys())[index-1]
        self._draw_plots()

    def _draw_plots(self):
        layout = self.simulator.layout()
        draw_networkx(self.simulator.graph(), ax=self.graph_plot.axes, pos=layout,
            node_color=PRIMARY_COLOR, edge_color=PRIMARY_COLOR, with_labels=False)
        draw_networkx_nodes(self.simulator.graph(), ax=self.graph_plot.axes, pos=layout, nodelist=['drain'], node_color='gray')
        self.graph_plot.axes.set_facecolor(BACKGROUND_COLOR)

        self.currency_plot.axes.cla()
        if self.__selected_currency is None:
            for curr_id in self.currency_storage:
                self.currency_plot.axes.plot(self.currency_storage[curr_id], label=self.currency_names[curr_id])
        else:
            curr_id = self.__selected_currency
            self.currency_plot.axes.plot(self.currency_storage[curr_id], label=self.currency_names[curr_id])
        self.currency_plot.axes.legend()
        self.currency_plot.axes.set_xlabel('Time Step')
        self.currency_plot.axes.set_ylabel('Currency Storage')
        self.currency_plot.axes.set_facecolor(BACKGROUND_COLOR)
        self.currency_plot.fig.subplots_adjust(bottom=0.2)
        self.currency_plot.draw()
