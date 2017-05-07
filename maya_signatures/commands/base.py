# maya_signatures/commands/base.py
"""The base structure for a CLI command."""


class Base(object):
    """A base command."""

    def __init__(self, *args, **kwargs):
        if args:
            if isinstance(args[0], dict):
                kwargs = args[0]
                kwargs['MAYA_CMDS'] = args[1:]
            else:
                maya_commands = kwargs.get('MAYA_CMDS', list(args))
                kwargs['MAYA_CMDS'] = maya_commands
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')