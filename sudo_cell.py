import sys, time

from PyQt4.QtCore import * 
from PyQt4.QtGui  import * 

from publisher import register_to_event
from publisher import trigger_event
from publisher import PUBLISHER_EVENT_SELECTION
from publisher import PUBLISHER_EVENT_INSERT
from publisher import PUBLISHER_EVENT_CLICKED

class sudo_Cell(QLineEdit):
	cell_size = 30
	font_size = 12
	selector_value = ''
	deletable = False

	def __init__(self, parent=None):
		QLineEdit.__init__(self,parent)
		self.defineGUI()

	def defineGUI(self):
		#size
		self.setFixedSize(self.cell_size, self.cell_size)
		self.setReadOnly(True)
		self.setContextMenuPolicy(Qt.NoContextMenu)
		self.setAlignment(Qt.AlignCenter)
		self.cellFormat()

		register_to_event(PUBLISHER_EVENT_SELECTION, self.insertSelection)

	def cellFormat(self, color='black'):
		self.setStyleSheet("""	QLineEdit{	font-size: %dpt;
											font-family: SansSerif;
											color: %s;}
								QLineEdit:hover { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);}""" 
							%(self.font_size, color))

	def insertSelection(self, value):
		#publisher event. set potential value for cell inside var
		self.selector_value = value[0]		 

	def mouseReleaseEvent(self, event):	
		trigger_event(PUBLISHER_EVENT_CLICKED, self)	

		_LR_click = event.button()
	
		if _LR_click == 1:
			'''LEFT CLICK'''			
			if not self.text() and self.selector_value != "x":
				self.set(self.selector_value)	#cell is blank. Set selector value to cell			
				self.cellFormat("red")			#redify newly set value			
				self.deletable = True			#set item as deletable
				
				trigger_event(PUBLISHER_EVENT_INSERT, self)	

			elif self.text() and self.selector_value == "x" and self.deletable:
				self.clear()
				self.deletable = False

		elif _LR_click == 2:
			'''RIGHT CLICK'''
			self.clear()
			self.deletable = False


	def get(self): 
		#get cell value here
		return str(self.text())

	def set(self, value):
		#set cell value here		
		self.setText(str(value))


class sudo_Box(QWidget):
	box_size = 0
	cells    = []

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.defineGUI()

		register_to_event(PUBLISHER_EVENT_CLICKED, self.clickEvent)
		register_to_event(PUBLISHER_EVENT_INSERT, self.itemAddedEvent)

	def defineGUI(self):
		#Cells		
		for idx in range(9):	
			exec("self.%s = sudo_Cell()" % ('cell_'+str(idx+1)))		
		
		#exec gil shit. to this like so for now
		self.cells = [self.cell_1, self.cell_2, self.cell_3, self.cell_4, self.cell_5, self.cell_6, self.cell_7, self.cell_8, self.cell_9]
		
		#Size		
		self.box_size 	= self.cell_1.cell_size*3
		self.setFixedSize(self.box_size, self.box_size)

		#Layout 
		layout = QGridLayout(self)	
		cell_idx = 0	
		for row in range(3):			
			for col in range(3):
				cell_idx += 1				
				exec("layout.addWidget(self.cell_%d, row, col)"%cell_idx)

		layout.setSpacing(0)
		layout.setContentsMargins(0,0,0,0)		

	def clickEvent(self, args):
		#restore color on click
		self.setStyleSheet("background: white")				

	def itemAddedEvent(self, args):
		item = args[0]
		
		__vals = []
		__flag = False
		for cell in self.cells:	
			__vals.append(cell.get())
			if cell == item:
				__flag = True


		if __flag:
			__current = item.get()
			__vals.remove(__current)
			__vals = filter(None, __vals)
			
			for __val in __vals:				
				if __val == __current:
					#reddify box
					self.setStyleSheet("background: rgba(250,0,0,50)")
		
		
class sudo_Matrix(QWidget):
	boxes_spacing = 4

	def __init__(self):
		QWidget.__init__(self)
		self.defineGUI()

	def defineGUI(self):
		#Boxes
		for idx in range(9):	
			exec("self.%s = sudo_Box()" % ('box_'+str(idx+1)))

		#Size		
		_matrix_size = self.box_1.box_size*3 + self.boxes_spacing*9
		self.setFixedSize(_matrix_size, _matrix_size)

		#Layout 
		layout = QGridLayout(self)	
		box_idx = 0	
		for row in range(3):			
			for col in range(3):
				box_idx += 1				
				exec("layout.addWidget(self.box_%d, row, col)"%box_idx)
		
		layout.setSpacing(self.boxes_spacing)


if __name__ == "__main__":
	app = QApplication(sys.argv)	
	frame = sudo_Matrix()	
	frame.show()		
	app.exec_()