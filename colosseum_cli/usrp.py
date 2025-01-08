import logging
import json
import time
import datetime
from colosseum_cli import colosseum_cli_constants as con
from colosseum_cli.colosseum_socket import connect_and_send
from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class usrp_info(Command):
    "Information on the USRP device"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(usrp_info, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('starting usrp info')
        # Read the radio map
        # Make the dictionary
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_USRP_INFO,
        }

        ret = connect_and_send(data_sent)
        if ret["status"] == 200:
            print(ret["message"])
        self.log.debug('completed usrp info')


class usrp_flash(Command):
    "Flash the USRP with a new UHD bitfile"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(usrp_flash, self).get_parser(prog_name)
        parser.add_argument('-f', '--filename', dest='filename', help='Filename of the UHD bitfile (has to be hosted in /share/usrp_images/)')
        parser.set_defaults(radio_map=None)
        return parser

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('starting RF scenario')
        # Read the radio map
        # Make the dictionary
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_USRP_FLASH,
        }

        if parsed_args.filename is not None:
            data_sent[con.USRP_FLASH_FILEPATH_KEY] = parsed_args.filename


        ret = connect_and_send(data_sent)
        print(ret["message"])
