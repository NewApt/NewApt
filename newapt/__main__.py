from sys import argv
from newapt.utils import CAT_ASCII, LION_ASCII, LION_ASCII2, DEBUG, esyslog
from newapt.fetch import fetch
from newapt.utils import logger, dprint, nodate_format, shell
from newapt.options import arg_parse
from newapt.newapt import newapt
import logging
from os import geteuid
from newapt import __version__
from getpass import getuser

def _main():
	parser = arg_parse()
	arguments = parser.parse_args()
	command = arguments.command
	debug = arguments.debug
	no_update = arguments.no_update
	assume_yes = arguments.assume_yes
	download_only = arguments.download_only
	verbose = arguments.verbose

	su = geteuid()
	if debug:
		std_err_handler = logging.StreamHandler()
		std_err_handler.setFormatter(nodate_format)
		logger.addHandler(std_err_handler)
		logger.setLevel(DEBUG)

	if not command:
		parser.print_help()
		exit()

	dprint(f"Argparser = {arguments}")

	superuser= ['update', 'upgrade', 'install', 'remove', 'fetch', 'clean']
	require_update = ['update', 'upgrade', 'install']
	no_update_list = ['remove', 'show', 'history']
	apt_init = ['update', 'upgrade', 'install', 'remove', 'show', 'history']

	if command in superuser:
		if su != 0:
			esyslog(f"{getuser()} tried to run [{' '.join(com for com in argv)}] without permission")
			exit(f"NewApt needs root to {command}")

	if command in apt_init:
		if command in no_update_list:
			no_update = True

		apt = newapt(
			download_only=download_only,
			assume_yes=assume_yes,
			no_update=no_update,
			debug=debug,
			verbose=verbose
		)

	if command in ['update', 'upgrade']:
		apt.upgrade(dist_upgrade=arguments.no_full)

	if command == 'install':
		args = arguments.args
		if not args:
			print('You must specify a package to install')
			exit()
		apt.install(args)

	if command == 'remove':
		args = arguments.args
		apt.remove(args)

	if command == 'fetch':
		foss = arguments.foss
		fetches = arguments.fetches
		debian = arguments.debian
		ubuntu = arguments.ubuntu
		country = arguments.country

		fetch(fetches, foss, debian, ubuntu, country, assume_yes)

	if command == 'show':
		args = arguments.args
		if not args:
			print('You must specify a package to show')
			exit()
		apt.show(args)

	if command == 'history':
		id = arguments.id
		mode = arguments.mode

		if mode:
			if not id:
				print('We need a transaction ID..')
				exit()
		else:
			apt.history()

		if mode in ['undo', 'redo', 'info']:
			try:
				id = int(id)
			except ValueError:
				print('Option must be a number..')
				exit()

		if mode == 'undo':
			apt.history_undo(id)

		elif mode == 'redo':
			apt.history_undo(id, redo=True)

		elif mode == 'info':
				apt.history_info(id)

		elif mode == 'clear':
			if su != 0:
				esyslog(f"{getuser()} tried to run [{' '.join(com for com in argv)}] without permission")
				exit(f"NewApt needs root to clear history")
			apt.history_clear(id)
	
	if command == 'clean':
		shell.apt.clean()
		print("NewApt's local cache has been cleaned up")

	if command == 'moo':
		moos = arguments.moo
		moos = moos.count('moo')
		dprint(f"moo number is {moos}")
		if moos == 1:
			print(LION_ASCII)
		elif moos == 2:
			print(LION_ASCII2)
		else:
			print(CAT_ASCII)
		print('..."I can\'t moo for I\'m a cat"...')
		if no_update:
			print("...What did you expect --no-update to do?...")

def main():
	try:
		_main()
	except KeyboardInterrupt:
		print('\nExiting at your request')
		exit()

