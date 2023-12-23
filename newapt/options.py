import argparse
from sys import argv
from pathlib import Path

class newaptParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        exit(1)

class newaptFormatter(argparse.RawDescriptionHelpFormatter):
    
    def format_help(self):
        help = self._root_section.format_help()
        if help:
            help = self._long_break_matcher.sub('\n\n', help)
            help = help.strip('\n') + '\n'
        if 'command:' in help:
            help = help.replace('\n\ncommand:\n', '\n\ncommand:')
        return help
    
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.RawTextHelpFormatter._split_lines(self, text, width)

def remove_options(parser, yes=True, download=True, update=True):
	for item in parser._optionals._group_actions[:]:
		if yes:
			if '--assume-yes' in item.option_strings:
				parser._optionals._group_actions.remove(item)
		if download:			
			if '--download-only' in item.option_strings:
				parser._optionals._group_actions.remove(item)
		if update:		
			if '--no-update' in item.option_strings:
				parser._optionals._group_actions.remove(item)

def arg_parse():

    formatter = lambda prog: newaptFormatter(prog, max_help_position=64)

    bin_name = Path(argv[0]).name

    global_options = newaptParser(add_help=False)
    global_options.add_argument('-y', '--assume-yes', action='store_true', help="assume 'yes' to all prompts and run non-interactively.")
    global_options.add_argument('-d', '--download-only', action='store_true', help="package files are only retrieved, not unpacked or installed")
    global_options.add_argument('-v', '--verbose', action='store_true', help='Logs extra information for debugging')
    global_options.add_argument('--no-update', action='store_true', help="skips updating the package list")
    global_options.add_argument('--debug', action='store_true', help='Logs extra information for debugging')

    parser = newaptParser(	formatter_class=formatter,
							usage=f'{bin_name} [--options] <command>',
							parents=[global_options]
							)

    subparsers = parser.add_subparsers(metavar='', dest='command')
    parser._subparsers.title = "command"
    parser._optionals.title = "options"

    fetch_options = newaptParser(add_help=False)
    fetch_options.add_argument('--fetches', metavar='number', type=int, default=3, help="number of mirrors to fetch")
    fetch_options.add_argument('--debian', metavar='sid', help="choose the Debian release")
    fetch_options.add_argument('--ubuntu', metavar='jammy', help="choose an Ubuntu release")
    fetch_options.add_argument('--country', metavar='"United States"', help="country must be as it appears on the mirror site. use quotes for spaces")
    fetch_options.add_argument('--foss', action='store_true', help="ommits contrib and non-free repos\n\n")

    fetch_parser = subparsers.add_parser('fetch',
		formatter_class=formatter,
		description=(
		'newapt will fetch mirrors with the lowest latency.\n'
		'for Debian https://www.debian.org/mirror/list-full\n'
		'for Ubuntu https://launchpad.net/ubuntu/+archivemirrors'
		),
		help='fetches fast mirrors to speed up downloads',
		parents=[fetch_options, global_options],
		usage=f'{bin_name} fetch [--options]'
	)

    remove_options(fetch_parser)

    fetch_parser._positionals.title = "arguments"
    fetch_parser._optionals.title = "options"

    return parser
