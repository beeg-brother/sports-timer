from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

plt.ion()
app = QApplication([])
app.setApplicationName("Sports Timer")
window = QWidget()
main_hbox = QHBoxLayout()
timer_vbox = QVBoxLayout()

main_hbox.addWidget(QPushButton('Top'))
updatePlotButton = QPushButton('UpdatePlot')
main_hbox.addWidget(updatePlotButton)
window.setLayout(main_hbox)

# create a new figure and canvas and add it to the main hbox
fig = Figure(figsize=(5,5))
dynamic_canvas = FigureCanvas(fig)
main_hbox.addWidget(dynamic_canvas)
# plot nothing to start off
laps = []
axes = dynamic_canvas.figure.add_subplot(111)
axes.plot(laps, 'r')
axes.set_title("Lap Statistics")

laps = [4,2,3,6,23,4,5,1,3,44,5,3,2,2,4,5,3,3,4,1,2,2,4,5,2,2,2,2,2,2,2,2,2,2,2,2,22]

# updates the statistics
def updatePlot(axes,data):
	# clear the current plot
	axes.cla()
	# plot the new data
	axes.plot(data,'r')
	# keep the title consistent
	axes.set_title("Lap Statistics")
	# update the plot
	fig.canvas.draw()
	fig.canvas.flush_events()

# update the plot when the button is clicked 
# this is just for testing the update function, eventually we're going to want to update
# everytime the lap button is hit
updatePlotButton.clicked.connect(lambda:updatePlot(axes,laps))

window.show()
app.exec_()