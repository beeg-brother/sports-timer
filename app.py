from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()
main_hbox = QHBoxLayout()
timer_vbox = QVBoxLayout()

layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec_()