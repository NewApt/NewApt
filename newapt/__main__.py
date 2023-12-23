from newapt.fetch import fetch
from newapt.options import arg_parse

def _main():
    parser = arg_parse()
    arguments = parser.parse_args()
    command = arguments.command
    assume_yes = arguments.assume_yes

    superuser= ['fetch']

    if command == 'fetch':
        foss = arguments.foss
        fetches = arguments.fetches
        debian = arguments.debian
        ubuntu = arguments.ubuntu
        country = arguments.country

        fetch(fetches, foss, debian, ubuntu, country, assume_yes)

def main():
    try:
        _main()
    except KeyboardInterrupt:
        print('\nExiting at your request')
        exit()
