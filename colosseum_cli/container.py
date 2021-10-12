import logging
import re
from cliff.command import Command
from colosseum_cli import colosseum_cli_constants as con
from colosseum_cli.colosseum_socket import connect_and_send


def img_name_fmt(str):
    """
    Validate img name for lxd container name restrictions
    Args:
        str:

    Returns:

    """
    if (re.match(r'^[A-Za-z0-9-]*$', str) is None) or len(str) > 32:
        print("Image name may only contain alphanumeric and hyphen characters. ")
        print("Max length is 32 characters ")
        raise ValueError
    else:
        return str


class container_snapshot(Command):
    "Create snapshot of the current container"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(container_snapshot, self).get_parser(prog_name)
        parser.add_argument('filename', type=img_name_fmt, help='Name of the image to be saved. '
                                                         'May only contain alphanumeric and hyphen.'
                                                           ' Max length is 32 characters')
        return parser

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        #print(parsed_args.filename)

        print('snapshotting the container to ' + parsed_args.filename + '.tar.gz')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_CTNR_SNAPSHOT,
            con.CLI_SNAPSHOT_FILE_KEY: parsed_args.filename,
            con.CLI_SNAPSHOT_PATH_KEY: con.CLI_SNAPSHOT_PATH
        }

        ret = connect_and_send(data_sent)
        print(ret['message'])
        self.log.debug('completed the snapshot')
