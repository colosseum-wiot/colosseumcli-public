import logging
import json
import time
import datetime
from colosseum_cli import colosseum_cli_constants as con
from colosseum_cli.colosseum_socket import connect_and_send
from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister

class tgen_start(Command):
    "Starts specified traffic scenario as soon as possible"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(tgen_start, self).get_parser(prog_name)
        parser.add_argument('scenario_id', type=int, help='ID of the traffic scenario')
        parser.add_argument('-m', '--node_map', dest='node_map', help='Json file that maps traffic nodes in the scenario to SRN IDs.')
        parser.set_defaults(node_map=None)
        return parser

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('starting traffic scenario')
        # Read the radio map
        # Make the dictionary
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_TGEN_START,
            con.CLI_SCEN_ID_KEY: parsed_args.scenario_id,
        }

        if parsed_args.node_map is not None:
            # Check the radio map
            try:
                node_map_str = open(parsed_args.node_map).read()
                node_map = json.loads(node_map_str)
            except:
                msg = "Failed to open json file " + parsed_args.node_map
                print(msg)
                return
            # Add the radio map to the json
            data_sent[con.CLI_SCEN_RADIO_MAP_KEY] = node_map

        ret = connect_and_send(data_sent)
        #print(ret)
        if ret["status"] == 200:
            msg = "Traffic Scenario " + str(parsed_args.scenario_id) + " started"
            print(msg)
        else:
            msg = "Colosseum failed to start traffic scenario: " + str(parsed_args.scenario_id)
            print(msg)
            print(ret["message"])

        self.log.debug('completed traffic scenario start')

class tgen_stop(Command):
    "Stops active traffic scenario"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('stopping traffic scenario')
        # Read the radio map
        # Make the dictionary
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_TGEN_STOP,
        }

        ret = connect_and_send(data_sent)
        #print(ret)
        if ret["status"] == 200:
            msg = "Traffic Scenario Stopped"
            print(msg)
        else:
            msg = "Colosseum failed to start traffic scenario"
            print(msg)
            print(ret["message"])

        self.log.debug('completed traffic scenario start')

class tgen_info(ShowOne):
    "Information on the active traffic scenario state."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('getting active TGEN info')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_TGEN_INFO
        }

        try:
            ret = connect_and_send(data_sent)
        except:
            rows = ('Scenario id',
                    'Status'
                    )
            values = ("", "")
            return(rows, values)

        #print(ret)
        if ret["status"] == 200:
            rows = ('Scenario id',
                    'Status'
                    )
            values = ("", "")

            if "data" in ret:
                session = ret["data"]
                #print(data)
                #print(session)
                values = (str(session['scenario_id']),
                        session['status']
                        )
                #print('completed traffic info')
        #TODO: temp fix for no session
        elif ret["status"] == 400:
            rows = ('Scenario id',
                    'Status'
                    )
            values = ("", "")
            print('No traffic sessions')
        else:
            print("Error getting scenario info. Code: " + str(ret["status"]))
            print(ret["message"])
            rows = ()
            values = ()

        return(rows, values)


class tgen_nodemap(Lister):
    "Information on the active traffic scenario state."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('getting active TGEN info')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_TGEN_INFO
        }
        rows = ('Node',
                'SRN'
                )
        nodes = [('None', 'None')]
        try:
            ret = connect_and_send(data_sent)
        except:
            #nodes = ()
            return(rows, nodes)

        #print(ret)
        if ret["status"] == 200:
            #nodes = ()

            if "data" in ret:
                session = ret["data"]
                #print(session)
                if "node_map" in session:
                    node_list = []
                    node_map = session["node_map"]
                    #print(node_map)
                    for key in node_map:
                        node_tup = (key,
                                    node_map[key]
                                    )

                        node_list.append(node_tup)
                    if len(node_list) > 0:
                        nodes = tuple(node_list)


        # TODO: temp fix for no session
        elif ret["status"] == 400:
            #nodes = ()
            print('No traffic sessions')
        else:
            print("Error getting scenario info. Code: " + str(ret["status"]))
            print(ret["message"])
            #nodes = ()
        return(rows, nodes)


class tgen_scenario_list(Lister):
    "List available TGEN scenario."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        #self.log.info('getting traffic scenario list')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_TGEN_LIST
        }

        ret = connect_and_send(data_sent)
        if ret['status'] == 200:
            data_rx = json.loads(ret['data'])
            #self.log.info(data_rx)
            scenarios_list = []
            for key in data_rx:
                scenario_dict = data_rx[key]
                #print(scenario_dict)
                title = "None"
                if "description" in scenario_dict:
                    title = scenario_dict["description"]

                scenario_tup = (scenario_dict["scenario_id"],
                                title,
                                )
                scenarios_list.append(scenario_tup)
            scenarios = tuple(scenarios_list)
            #self.log.info('completed scenario list')
        else:
            print("Failed to get the scenario list. Code: " + str(ret['status']))
            print(ret["message"])
            scenarios = ()

        return (("Scenario ID", "Description"), scenarios)
