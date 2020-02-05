from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

plt.ion()
app = QApplication([])
window = QWidget()
main_hbox = QHBoxLayout()
timer_vbox = QVBoxLayout()

layout.addWidget(QPushButton('Top'))
updatePlotButton = QPushButton('UpdatePlot')
layout.addWidget(updatePlotButton)
window.setLayout(layout)


fig = Figure(figsize=(5,5))
dynamic_canvas = FigureCanvas(fig)
layout.addWidget(dynamic_canvas)

laps = [4,2,3,6,23,4,5,1,3,44,5,3,2]

axes = dynamic_canvas.figure.add_subplot(111)
axes.plot(laps, 'r-')
axes.set_title("Lap Statistics")
laps = [4,2,3,6,23,4,5,1,3,44,5,3,2,2,4,5,3,3,4,1,2,2,4,5,2,2,2,2,2,2,2,2,2,2,2,2,22]


def updatePlot(axes,data):
	axes.cla()
	axes.plot(laps,'r-')
	fig.canvas.draw()
	fig.canvas.flush_events()

updatePlotButton.clicked.connect(lambda:updatePlot(axes,laps))

window.show()
app.exec_()