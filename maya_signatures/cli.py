"""
mayasig.

Usage:
  mayasig [-m|--mayaversion VERSION] [-d|--depth DEPTH] (MAYA_CMDS ...)
  mayasig (-h|--help)
  mayasig (--version)

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -m VERSION --mayaversion VERSION  If you want to override which Maya docs we query (tested with 2015/2016/2017) [default: 2017]
  -d DEPTH --depth DEPTH            The depth verbosity of the return dictionary [default: 1]
  MAYA_CMDS                         Maya commands to query/scrape from the help and return signatures for

Examples:
  mayasig group

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/andresmweber/mayasig-cli
"""

import commands as maya_signature_commands
import docopt
from pprint import pprint
import sys
from inspect import getmembers, isclass


def main():
    """Main CLI entry point."""
    try:
        arguments = docopt.docopt(__doc__)
    except docopt.DocoptExit:
        print('invalid operation. %s' % str(sys.argv[1:]))
        raise

    has_run = False
    for command in list(arguments):
        if hasattr(maya_signature_commands, command):
            module = getattr(maya_signature_commands, command)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command(arguments)
            has_run = True

    if not has_run:
        print('No command entered, defaulting to query mode for commands: %s' % ' '.join(arguments['MAYA_CMDS']))
        pprint(maya_signature_commands.scrape.Scrape(arguments), depth=3)
