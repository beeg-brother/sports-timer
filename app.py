from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from threading import Lock, Thread
from time import time_ns, sleep
from datetime import timedelta as time_format

plt.ion()
app = QApplication([])
app.setApplicationName("Sports Timer")
window = QWidget()

current_time = 0
last_lap = 0


main_vbox = QVBoxLayout()

main_vbox.addStretch(1)

timer_label = QLabel(str(time_format(milliseconds = 0)))
main_vbox.addWidget(timer_label)

main_vbox.addStretch(.25)

timer_button_hbox = QHBoxLayout()
start_button = QPushButton('Start')
pause_button = QPushButton('Pause')
lap_button = QPushButton('Lap')
reset_button = QPushButton('Reset')
resume_button = QPushButton('Start')

timer_button_hbox.addWidget(lap_button)
timer_button_hbox.addWidget(start_button)

main_vbox.addLayout(timer_button_hbox)


stats_hbox = QHBoxLayout()
main_vbox.addLayout(stats_hbox)

# create a new figure and canvas and add it to the main hbox
fig = Figure(figsize=(5,5))
dynamic_canvas = FigureCanvas(fig)
# plot nothing to start off
laps = []
axes = dynamic_canvas.figure.add_subplot(111)
axes.plot(laps, 'r')
axes.set_title("Lap Statistics")
stats_hbox.addWidget(dynamic_canvas)

window.setLayout(main_vbox)

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


def truncate(num, decs):
	div = 10 ** decs
	return int(num*div) / div

timer_lock = Lock()

def counter():
	global current_time
	while(True):
		timer_lock.acquire()
		timer_lock.release()
		start_time = time_ns()
		sleep(.05)
		current_time += time_ns() - start_time
		timer_label.setText(str(time_format(seconds = truncate(current_time/1000000000, 2)))[:-4])


timer = Thread(name='timer', target = counter)

def start_helper():
	timer.start()
	start_button.setParent(None)
	timer_button_hbox.addWidget(pause_button)

start_button.clicked.connect(start_helper)

def pause_helper():
	timer_lock.acquire()
	pause_button.setParent(None)
	timer_button_hbox.removeWidget(lap_button)
	lap_button.setParent(None)
	timer_button_hbox.addWidget(reset_button)
	timer_button_hbox.addWidget(resume_button)
		
pause_button.clicked.connect(pause_helper)

def resume_helper():
	timer_lock.release()
	resume_button.setParent(None)
	reset_button.setParent(None)
	timer_button_hbox.addWidget(lap_button)
	timer_button_hbox.addWidget(pause_button)

resume_button.clicked.connect(resume_helper)

def reset_helper():
	global current_time
	global laps
	global last_lap
	current_time = 0
	last_lap = 0
	reset_button.setParent(None)
	resume_button.setParent(None)
	timer_button_hbox.addWidget(lap_button)
	timer_button_hbox.addWidget(resume_button)
	timer_label.setText(str(time_format(milliseconds = 0)))
	laps = []
	updatePlot(axes, laps)

reset_button.clicked.connect(reset_helper)

def lap_helper():
	global current_time
	global last_lap
	time_lap_button_clicked = current_time
	delta_time = time_lap_button_clicked - last_lap
	if delta_time > 0:
		laps.append((current_time - last_lap)/1000000000)
		last_lap = current_time
		updatePlot(axes, laps)

lap_button.clicked.connect(lap_helper)

window.show()
app.exec_()