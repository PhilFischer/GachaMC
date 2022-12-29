"""Simulation Window UI"""

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel

from ui.constants import BACKGROUND_COLOR
from gmc.flow_model import FlowModel
from gmc.mc_simulator import Simulator

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):
    """Matplotlib Canvas Class"""

    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=BACKGROUND_COLOR)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class SimulationWindow(QWidget):
    """Simulation Window Class"""

    def __init__(self, model: FlowModel):
        super().__init__(parent=None)
        self.simulator = Simulator(model.copy())

        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("Monte Carlo Simulation")
        self.setMinimumHeight(480)
        self.setMinimumWidth(720)

        title = QLabel("Monte Carlo Simulation")
        title.setStyleSheet('font-size: 24pt;')
        layout.addWidget(title, 0, 0)

        plot = MplCanvas()
        self.simulator.draw_flow_graph(plot.axes)
        layout.addWidget(plot, 1, 0)

        info = QVBoxLayout()
        flow = self.simulator.compute_max_flow()
        if flow['status'] == 0:
            max_panel = QLabel(f"Target Time: {flow['steps']} time steps")
            max_panel.setStyleSheet('font-size: 14pt;')
            info.addWidget(max_panel)
            status_panel = QLabel(flow['message'])
            status_panel.setWordWrap(True)
            status_panel.setStyleSheet('background-color: green; padding: 8px 5px 8px 5px;')
            info.addWidget(status_panel)
        else:
            status_panel = QLabel(flow['message'])
            status_panel.setWordWrap(True)
            status_panel.setStyleSheet('background-color: green; padding: 8px 5px 8px 5px;')
            info.addWidget(status_panel)
        info.addStretch()
        info_widget = QWidget()
        info_widget.setLayout(info)
        layout.addWidget(info_widget, 1, 1)
