import sys
from colosseum_cli import colosseum_cli_constants as con
from cliff.app import App
from cliff.commandmanager import CommandManager


class ColCliApp(App):
    def __init__(self):
        super(ColCliApp, self).__init__(
            description='colosseum cli app',
            version=con.CLI_APP_VERION,
            command_manager=CommandManager('cliff.colosseum'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = ColCliApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
