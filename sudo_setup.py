import py2exe
import sys
from   distutils.core import setup

sys.argv.append('py2exe')

setup(
  name         = 'Mirco Sudoku',
  version      = '1.0',
  description  = 'Mirco Sudoku Game',
  author       = 'Garjitzky Cristian',
  windows	   = [{
                  "script":"MircoSudoku.py",
                  "icon_resources": [(1, "sudoku_icon.ico")],
                  }],
  data_files   = ['menu.png', 'sudoku.png','configuration.ini'],
  options	   = {"py2exe":{"includes":["sip"]}},
)


