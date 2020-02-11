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

lapTime = 0
currLap_label = QLabel(str(time_format(milliseconds = 0)))
lastLap_label = QLabel(str(time_format(milliseconds = 0)))
main_vbox.addWidget(timer_label)
main_vbox.addWidget(currLap_label)

main_vbox.addStretch(.25)

# define the area where the buttons are
timer_button_hbox = QHBoxLayout()
# create the button objects
start_button = QPushButton('Start')
pause_button = QPushButton('Pause')
lap_button = QPushButton('Lap')
reset_button = QPushButton('Reset')
resume_button = QPushButton('Start')
# add the two buttons that we start with, laps and starting the timer
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
# add the canvas to the gui
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
# defines the loop that increments the time
def counter():
	global current_time
	while(True):
		timer_lock.acquire()
		timer_lock.release()
		start_time = time_ns()
		sleep(.05)
		current_time += time_ns() - start_time
		current_lap_time = current_time - last_lap
		# modify the label of the timer
		timer_label.setText(str(time_format(seconds = truncate(current_time/1000000000, 2)))[:-4])
		currLap_label.setText(str(time_format(seconds = truncate(current_lap_time/1000000000, 2)))[:-4])


# define the timer thread
timer = Thread(name='timer', target = counter)

# what to do when someone hits the start button
def start_helper():
	timer.start()
	start_button.setParent(None)
	timer_button_hbox.addWidget(pause_button)

start_button.clicked.connect(start_helper)
# what to do when someone hits the pause button
def pause_helper():
	timer_lock.acquire()
	pause_button.setParent(None)
	timer_button_hbox.removeWidget(lap_button)
	lap_button.setParent(None)
	timer_button_hbox.addWidget(reset_button)
	timer_button_hbox.addWidget(resume_button)
		
pause_button.clicked.connect(pause_helper)
# what to do when someone hits the resume button
def resume_helper():
	timer_lock.release()
	resume_button.setParent(None)
	reset_button.setParent(None)
	timer_button_hbox.addWidget(lap_button)
	timer_button_hbox.addWidget(pause_button)

resume_button.clicked.connect(resume_helper)

# what to do when someone hits the reset button
def reset_helper():
	global current_time
	global laps
	global last_lap
	current_time = 0
	last_lap = 0
	# get rid of the reset and resume buttons
	reset_button.setParent(None)
	resume_button.setParent(None)
	# add the lap and resume buttons
	timer_button_hbox.addWidget(lap_button)
	timer_button_hbox.addWidget(resume_button)
	# update the timer count
	timer_label.setText(str(time_format(milliseconds = 0)))
	currLap_label.setText(str(time_format(milliseconds = 0)))
	# reset the lap data
	laps = []
	# update the chart
	updatePlot(axes, laps)

reset_button.clicked.connect(reset_helper)
# what to do when someone hits the lap button
def lap_helper():
	global current_time
	global last_lap
	time_lap_button_clicked = current_time
	delta_time = time_lap_button_clicked - last_lap
	# check to make sure that the timer is actually running
	if delta_time > 0:
		# add to the lap data
		lapTime = current_time - last_lap
		laps.append((lapTime)/1000000000)
		#add spot to show the last lapTime
		last_lap = current_time
		# plot the new  stats
		updatePlot(axes, laps)

lap_button.clicked.connect(lap_helper)

window.show()
app.exec_()