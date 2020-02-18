#!/usr/bin/python3
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from threading import Lock, Thread
from time import time_ns, sleep
from datetime import timedelta as time_format
from statistics import mean


plt.ion()
app = QApplication([])
app.setApplicationName("Sports Timer")
window = QWidget()

current_time = 0
last_lap = 0
lapTime = 0

main_vbox = QVBoxLayout()

main_vbox.addStretch(1)

timer_label = QLabel(str(time_format(milliseconds = 0)))
# Center the timer
timer_label.setAlignment(QtCore.Qt.AlignCenter)
# set the font to be large and bold for the real timer
big_font = QtGui.QFont("Times", 38, QtGui.QFont.Bold)
timer_label.setFont(big_font)

# add the timers to the gui
main_vbox.addWidget(timer_label)

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

# create the lower area for stats
laps_hbox = QHBoxLayout()
main_vbox.addLayout(laps_hbox)

# add the table to the vbox
laptime_table = QTableWidget()

# set up the table properly, current_lap_num for later use
current_lap_num = 1
laptime_table.setEditTriggers(QTableWidget.NoEditTriggers)
laptime_table.setRowCount(1)
laptime_table.setColumnCount(1)
laptime_table.setItem(0, 0, QTableWidgetItem("0:00:00.00"))
laptime_table.setVerticalHeaderItem(0, QTableWidgetItem("Current lap"))

header = laptime_table.horizontalHeader()
header.setSectionResizeMode(QHeaderView.ResizeToContents)
header.setStretchLastSection(True)

laptime_table.setHorizontalHeaderLabels(["Lap time"])

laps_hbox.addWidget(laptime_table)

# area for the stats graph and below it, avg/fast/slow
stats_vbox = QVBoxLayout()
laps_hbox.addLayout(stats_vbox)

# create a new figure and canvas and add it to the stats hbox
fig = Figure(figsize=(1.5,1.5), tight_layout=True, frameon=False)
dynamic_canvas = FigureCanvas(fig)
# plot nothing to start off
laps = []
axes = dynamic_canvas.figure.add_subplot(111)
axes.plot(laps, ' ')
axes.axis('off')
# add the canvas to the gui
stats_vbox.addWidget(dynamic_canvas)

# area to organize the avg/fast/slow labels
data_hbox = QHBoxLayout()
stats_vbox.addLayout(data_hbox)

# area for the avg/fast/slow labels to go
data_labels_vbox = QVBoxLayout()
data_hbox.addLayout(data_labels_vbox)

# labels for the stats
avg_lap_name_label = QLabel("Average lap:")
fastest_lap_name_label = QLabel("Fastest lap:")
slowest_lap_name_label = QLabel("Slowest lap:")

data_labels_vbox.addWidget(avg_lap_name_label)
data_labels_vbox.addWidget(fastest_lap_name_label)
data_labels_vbox.addWidget(slowest_lap_name_label)

# area for the actual stats
data_actual_vbox = QVBoxLayout()
data_hbox.addLayout(data_actual_vbox)

# labels for the actual stats
avg_lap_label = QLabel("0:00:00.00")
fastest_lap_label = QLabel("0:00:00.00")
slowest_lap_label = QLabel("0:00:00.00")

data_actual_vbox.addWidget(avg_lap_label)
data_actual_vbox.addWidget(fastest_lap_label)
data_actual_vbox.addWidget(slowest_lap_label)

window.setLayout(main_vbox)

# updates the statistics
def updatePlot(axes,data):
	# clear the current plot
	axes.cla()
	# plot the new data
	axes.plot(data,' ')
	axes.axis('off')
	# color the space underneath our plot blue
	axes.fill_between(range(len(data)), data, color='#6694f6cc')
	# update the plot
	fig.canvas.draw()
	fig.canvas.flush_events()


def truncate(num, decs):
	div = 10 ** decs
	return int(num*div) / div + .0001

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
		# modify the current lap timer
		laptime_table.setItem(0, 0, QTableWidgetItem(str(time_format(seconds = truncate(current_lap_time/1000000000, 2)))[:-4]))

# define the timer thread
timer = Thread(name='timer', target = counter)
# make it so that we can close the thread nicely
timer.daemon = True

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
	global current_lap_num
	current_time = 0
	last_lap = 0
	current_lap_num = 1
	# get rid of the reset and resume buttons
	reset_button.setParent(None)
	resume_button.setParent(None)
	# add the lap and resume buttons
	timer_button_hbox.addWidget(lap_button)
	timer_button_hbox.addWidget(resume_button)
	# update the timer count
	timer_label.setText(str(time_format(milliseconds = 0)))

	# reset the lap data
	laps = []
	# update the chart
	updatePlot(axes, laps)
	avg_lap_label.setText("0:00:00.00")
	slowest_lap_label.setText("0:00:00.00")
	fastest_lap_label.setText("0:00:00.00")

	#reset table
	laptime_table.setRowCount(0)
	laptime_table.insertRow(0)
	laptime_table.setItem(0, 1, QTableWidgetItem("0:00:00.00"))
	laptime_table.setVerticalHeaderItem(0, QTableWidgetItem("Current lap"))
reset_button.clicked.connect(reset_helper)

# what to do when someone hits the lap button
def lap_helper():
	global current_time
	global last_lap
	global lapTime
	global laps
	global current_lap_num
	time_lap_button_clicked = current_time
	delta_time = time_lap_button_clicked - last_lap
	# check to make sure that the timer is actually running
	if delta_time > 0:
		# add to the lap data
		lapTime = (current_time - last_lap)/1000000000
		laps.append(lapTime)

		last_lap = current_time
		# plot the new  stats
		updatePlot(axes, laps)
		avg_lap_label.setText(str(time_format(seconds = truncate(mean(laps), 2)))[:-4])
		slowest_lap_label.setText(str(time_format(seconds = truncate(max(laps), 2)))[:-4])
		fastest_lap_label.setText(str(time_format(seconds = truncate(min(laps), 2)))[:-4])
		# add lap time to lap time table
		laptime_table.insertRow(1)
		laptime_table.setItem(0, 1, QTableWidgetItem(str(time_format(seconds = truncate(lapTime, 2)))[:-4]))
		# Always scroll to the newest data point in the table
		laptime_table.scrollToItem(laptime_table.itemAt(0,0))
		#label the row properly
		lap_num_label = str("Lap " + str(current_lap_num))
		current_lap_num += 1
		laptime_table.setVerticalHeaderItem(1, QTableWidgetItem(lap_num_label))
lap_button.clicked.connect(lap_helper)

window.show()
window.setFixedSize(window.width(), window.height())
app.exec_()