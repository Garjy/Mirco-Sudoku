import sys

from PyQt4.QtCore import * 
from PyQt4.QtGui  import * 

from publisher import register_to_event
from publisher import PUBLISHER_EVENT_INSERT

from sudo_selector 	import sudo_Selector
from sudo_cell 		import sudo_Matrix, sudo_Cell

from sudoku_generate import generator, set_dificulty

def load_cfg():
	#load mirco sudoku configuration
	file = open("configuration.ini", "r")
	raw = file.read()
	file.close()

	return raw

def save_cfg(content):
	#save mirco sudoku configuration
	file = open("configuration.ini", "w")
	file.write(str(content))
	file.close()

class sudo_Toolbar(QToolBar):
	def __init__(self):
		QToolBar.__init__(self)
		self.setObjectName("Sudoku toolbar")
		self.setFloatable(False)
		self.setMovable(False)
		self.setIconSize(QSize(32, 32))
		self.setToolButtonStyle(Qt.ToolButtonIconOnly)

		self.setStyleSheet("background:gray")

		self.setWindowOpacity(0.6)
	
		self.menu_action = self.addAction(QIcon("menu.png"),"Menu")
		
		spacer = QWidget()					#add expanding spacer in toolbar
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(spacer)
	
class sudo_Settings(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self)
		self.parent = parent

		self.define_GUI()

	def define_GUI(self):
		self.setStyleSheet("background: gray")
		self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

		#slider
		__dificulty_lb = QLabel('Dificulty')		
		self.dificulty = QSlider(Qt.Horizontal)
		self.dificulty.setMaximumWidth(150)
		self.dificulty.setMinimum(1)
		self.dificulty.setMaximum(50)
		#self.dificulty.setEnabled(False)
		self.dificulty.sliderReleased.connect(self.handleDificulty)

		self.dificulty_input = QLineEdit()
		self.dificulty_input.setFixedWidth(20)
		self.dificulty_input.setReadOnly(True)
		#self.dificulty_input.returnPressed.connect(self.handleDificulty)

		spacer = QWidget()					#add expanding spacer in toolbar
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		layout = QHBoxLayout(self)
		layout.addWidget(__dificulty_lb)
		layout.addWidget(self.dificulty)
		layout.addWidget(self.dificulty_input)
		layout.addWidget(spacer)

		# Animation
		self._animation = QPropertyAnimation(self, "size")
		self._animation.setDuration(500)
		self._animation.setEasingCurve(QEasingCurve.Linear)

	def showEvent(self, event):
		self._animation.setStartValue(QSize(self.parent.width(),0))		
		self._animation.setEndValue(QSize(self.parent.width(),40))
		self._animation.start()
		
		self.parent.settings.resize(self.parent.width(), 40)				#resize dock
		
	def handleDificulty(self):	
		difi = self.dificulty.value()
		#difi = int(self.dificulty_input.text())
		self.dificulty_input.setText(str(difi))

		set_dificulty(difi)				#set dificulty for algorithm generation
		self.parent.populate_matrix()	#repopulate sudoku matrix from algorithm

		save_cfg(difi)


class sudo_main(QMainWindow):
	solution = []
	settings_visible = False

	def __init__(self):
		QMainWindow.__init__(self)
		self.define_GUI()
		dificulty = int(load_cfg())										#get dificulty from cfg
		set_dificulty(dificulty)										#set dificulty to algorithm
		self.settings_widget.dificulty_input.setText(str(dificulty))	#set dificulty_input value
		self.settings_widget.dificulty.setValue(int(dificulty))			#set dificulty slider value
		self.populate_matrix()

	def define_GUI(self):
		self.resize(500,500)

		#Toolbar
		self.toolbar = sudo_Toolbar()
		self.toolbar.resize(200,100)
		self.addToolBar(Qt.TopToolBarArea , self.toolbar)
		self.toolbar.menu_action.triggered.connect(self.handleSettings)

		#Widgets
		self.matrix 	= sudo_Matrix()
		self.selector 	= sudo_Selector()		
		
		self.settings   = QDockWidget('  Settings')
		self.settings_widget = sudo_Settings(self)
		self.settings.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.settings.setWidget(self.settings_widget)
		self.addDockWidget(Qt.TopDockWidgetArea, self.settings )

		self.settings.hide()

		#Center Widget
		center_widget = QWidget()
		layout = QVBoxLayout(center_widget)
		layout.addWidget(self.matrix)
		layout.addWidget(self.selector)
		layout.setAlignment(Qt.AlignHCenter)

		self.setCentralWidget(center_widget)

		register_to_event(PUBLISHER_EVENT_INSERT, self.itemAddedEvent)

	def handleSettings(self):
		if self.settings_visible:
			self.settings.hide()
			self.settings_visible = False
		else:
			self.settings.show()
			self.settings_visible = True

	def populate_matrix(self):
		'''clear matrix and populate with sudoku puzzle from generator'''
		self.clear_matrix()

		sudoku = generator()
		_sudo_solved_matrix = sudoku[0]					#generate sudoku matrix SOLVED
		_sudo_matrix 		= sudoku[1]					#generate sudoku matrix with blanks

		self.solution = _sudo_solved_matrix				#store matrix solution

		_cells = self.findChildren(sudo_Cell)			#get all cell objects
		for _idx,_cell in enumerate(_cells): 
			_val = _sudo_matrix[_idx]
			if _val > 0:
				_cell.set(_val)

	def clear_matrix(self):
		_cells = self.findChildren(sudo_Cell)			#get all cell objects
		for _cell in _cells:
			_cell.clear()

	def get_curent_matrix(self):
		_matrix = []
		_ready_flag = True
		
		_cells = self.findChildren(sudo_Cell)			#get all cell objects
		for _cell in _cells:
			try:
				_cell_val 	= int(_cell.get())			#convert value to int. except when blank
			except:
				_cell_val 	= 0							#replace blank item with 0
				_ready_flag = False						#if blank items still exist matrix is not ready for checking

			_matrix.append(_cell_val)

		return _matrix, _ready_flag

	def itemAddedEvent(self, args):
		'''Added new value in a cell'''
		_matrix, _ready = self.get_curent_matrix()		
		if _ready:
			if _matrix == self.solution:
				"""Show popup when completed puzzle"""
				_popup = QMessageBox(self)
				_popup.setText("Bravo! You finished the Sudoku puzzle")
				_popup.setWindowTitle("Finished")
				_popup.show()

	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("sudoku.png"))	
	frame = sudo_main()	
	frame.setWindowTitle('MircoSudoku')
	frame.show()		
	app.exec_()