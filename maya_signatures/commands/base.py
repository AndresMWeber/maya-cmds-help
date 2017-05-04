# maya_signatures/commands/base.py
"""The base command."""


class Base(object):
    """A base command."""

    def __init__(self, *args, **kwargs):
        print 'storing args ', args, ' storing kwargs ', kwargs
        if isinstance(args[0], dict):
            kwargs = args[0]
            args = args[1:]
        else:
            maya_commands = kwargs.get('MAYA_CMDS', list(args))
            kwargs['MAYA_CMDS'] = maya_commands
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')