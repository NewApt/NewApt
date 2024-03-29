from logging.handlers import RotatingFileHandler, SysLogHandler
from os import geteuid, devnull
from pyshell import pyshell
from pathlib import Path
import logging

LICENSE = Path('/usr/share/common-licenses/GPL-3')
"""/usr/share/common-licenses/GPL-3"""
NEWAPT_SOURCES = Path('/etc/apt/sources.list.d/newapt-sources.list')
"""/etc/apt/sources.list.d/newapt-sources.list"""
NEWAPT_LOGDIR = Path('/var/log/newapt')
"""/var/log/newapt"""
NEWAPT_LOGFILE = NEWAPT_LOGDIR / 'newapt.log'
"""/var/log/newapt/newapt.log"""
NEWAPT_DEBUGLOG = NEWAPT_LOGDIR / 'newapt-debug.log'

shell = pyshell(capture_output=True, text=True, check=True)

# Define log levels for import
INFO = 20
DEBUG = 10

# Click Style Colors
RED = {'fg':'red', 'bold':True}
YELLOW = {'fg':'yellow', 'bold':True}
GREEN = {'fg':'green', 'bold':True}
BLUE = {'fg':'blue', 'bold':True}
CYAN = {'fg':'cyan', 'bold':True}
MAGENTA = {'fg':'magenta', 'bold':True}

# Create our main logger. This will do nothing unless we're root
logger = logging.getLogger('newapt_logger')
logger.setLevel(INFO)

# Define logging formatters
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')
sys_formatter = logging.Formatter('newapt: %(levelname)s: %(message)s')
nodate_format = logging.Formatter('[%(levelname)s]: %(message)s')
empty_format = logging.Formatter('%(message)s')

# Our syslogger. Currently only used for telling on people for using trying to use newapt without permission
syslogger = logging.getLogger('newapt_syslogger')
syslogger.setLevel(INFO)
syslog_handler = SysLogHandler(facility=SysLogHandler.LOG_USER, address='/dev/log')
syslog_handler.setFormatter(sys_formatter)
syslogger.addHandler(syslog_handler)

if geteuid() == 0:
	from newapt.options import arg_parse
	parser = arg_parse()
	arguments = parser.parse_args()
	verbose = arguments.verbose
	debug = arguments.debug

	if not NEWAPT_LOGDIR.exists():
		NEWAPT_LOGDIR.mkdir()
	if debug:
		file_handler = RotatingFileHandler(NEWAPT_DEBUGLOG, maxBytes=1024*1024, backupCount=10)
	else:
		file_handler = RotatingFileHandler(NEWAPT_LOGFILE, maxBytes=1024*1024, backupCount=10)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
else:
	file_handler = RotatingFileHandler(devnull, maxBytes=1024*1024, backupCount=10)

syslog = syslogger.info
esyslog = syslogger.error

eprint = logger.error
iprint = logger.info
dprint = logger.debug

def logger_newline():
	file_handler.setFormatter(empty_format)
	iprint('')
	file_handler.setFormatter(formatter)

def ask(question, default_no=False):
	"""resp = input(f'{question}? [Y/n]

	Y returns True
	N returns False
	"""
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
			print("Not a valid choice kiddo")


LION_ASCII = (
r"""
         |\_
       -' | \
      /7     \
     /        `-_
     \-'_        `-.____________
      -- \                 /    `.
         /                 \      \
 _______/    /_       ______\      |__________-
(,__________/  `-.___(,_____________----------_)
"""
)
# I couldn't find an artist for these. If anyone knows let me know.
# I love to give credit when I can
LION_ASCII2 = (
r"""
    |\_
  -' | `.
 /7      `-._
/            `-.____________
\-'_                        `-._
 -- `-._                    |` -`.
       |\               \   |   `\\
       | \  \______...---\_  \    \\
       |  \  \           | \  |    ``-.__--.
       |  |\  \         / / | |       ``---'
     _/  /_/  /      __/ / _| |
    (,__/(,__/      (,__/ (,__/
"""
)

CAT_ASCII = (
r"""
   |\---/|
   | ,_, |
    \_`_/-..----.
 ___/ `   ' ,""+ \  sk
(__...'   __\    |`.___.';
  (_,...'(_,.`__)/'.....+
"""
)