import os
import sys
import time

from PyQt4.QtCore import * 
from PyQt4.QtGui  import * 

from publisher import trigger_event
from publisher import PUBLISHER_EVENT_SELECTION


# Selector #

class sudo_Selector(QWidget):
	selection = "x"
	_button_size = QSize(30,30)
	def __init__(self):
		QWidget.__init__(self)
		self.defineGUI()
			

	def defineGUI(self):
		__children = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
		# Degine Buttons Style # spare : font-weight: bold; #
		self.setStyleSheet("""QPushButton {	font-size: 12pt; 
											font-family: SansSerif;											
											color: rgb(70,70,70);   
											border: 1px solid #8f8f91;    
											border-radius: 4px;
											background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde);}
							QPushButton:hover { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}
							QPushButton:pressed { border-color: rgb(70,70,70);}
							QPushButton:on {color: black; background-color: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #cce0ff, stop :  1.0 #66a3ff);padding-top: 1px;}""")
		
		#Group Buttons#
		self.group = QButtonGroup(self)
		self.group.setExclusive(True)
		self.group.buttonReleased.connect(self.handleSelect)
		
		# X #		
		delete = QPushButton("x",self)
		delete.setCheckable(True)		
		delete.setFixedSize(self._button_size)
		delete.setStyleSheet("""QPushButton {background-color: #ffb3b3; } 
								QPushButton:on {color: black; background-color: #ff3333 ;padding-top: 1px;}""")
		self.group.addButton(delete)
		__distance = self._button_size.width()+1		

		#Number Buttons
		for __idx,__child in enumerate(__children, 1):	
			exec("%s = QPushButton('%d',self)" % (__child, __idx))	
			exec("%s.setCheckable(%s)" %(__child, 'True'))
			exec("%s.move(%d, %d)" %(__child, __distance, 0))
			exec("%s.setFixedSize(self._button_size)" %(__child))
			exec("self.group.addButton(%s)" %(__child))
			__distance += self._button_size.width()+1

		self.setFixedSize(__distance, delete.height())	
		
	def showEvent(self, event):
		self.animateButtons()			#execute animation upon showing	

	def animateButtons(self):		
		for _idx in range(10):	 
			_time = (200 * _idx) + 50
			FaderWidget(QWidget(), self.group.buttons()[_idx], _time)

	def handleSelect(self, button):
		_sel = button.text()
		self.selection = str(_sel)				
		trigger_event(PUBLISHER_EVENT_SELECTION, self.selection)				#send data to the publisher	

class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget, time=0):
    
        QWidget.__init__(self, new_widget)
        
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
       
        #self.timeline.setDuration(random.randint(100,1000))        
        self.timeline.setDuration(int(time))
        self.timeline.start()
        
        self.resize(new_widget.size())
        self.show()
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()
    
    def animate(self, value):
    
        self.pixmap_opacity = 1.0 - value
        self.repaint()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = sudo_Selector()
	
	win.show()
	app.exec_()