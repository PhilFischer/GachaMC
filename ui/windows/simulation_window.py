"""Simulation Window UI"""

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel

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
        self._simulator = Simulator(model)

        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("Monte Carlo Simulation")
        self.setMinimumHeight(480)
        self.setMinimumWidth(720)

        title = QLabel("Monte Carlo Simulation")
        title.setStyleSheet('font-size: 24pt;')
        layout.addWidget(title, 0, 0)

        plot = MplCanvas()
        self._simulator.draw_flow_graph(plot.axes)
        layout.addWidget(plot, 1, 0)

        plot2 = MplCanvas()
        self._simulator.draw_flow_graph(plot2.axes)
        layout.addWidget(plot2, 1, 1)
