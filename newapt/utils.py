from pyshell import pyshell
from pathlib import Path
import logging

NEWAPT_SOURCES = Path('/etc/apt/sources.list.d/newapt-sources.list')

shell = pyshell(capture_output=True, text=True, check=True)

INFO = 20

RED = {'fg':'red', 'bold':True}
YELLOW = {'fg':'yellow', 'bold':True}
GREEN = {'fg':'green', 'bold':True}
BLUE = {'fg':'blue', 'bold':True}

logger = logging.getLogger('newapt_logger')
logger.setLevel(INFO)

dprint = logger.debug

def ask(question, default_no=False):
	while True:
		resp = input(f'{question}? [Y/n] ')
		if resp in ['y', 'Y']:
			return True
		elif resp in ['n', 'N']:
			return False
		elif resp == '':
			if default_no:
				return False
			return True
		else:
			print("Not a valid choice")
