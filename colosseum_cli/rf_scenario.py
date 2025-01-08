import logging
import json
import time
import datetime
from colosseum_cli import colosseum_cli_constants as con
from colosseum_cli.colosseum_socket import connect_and_send
from cliff.command import Command
from cliff.show import ShowOne
from cliff.lister import Lister


class rf_scenario_start(Command):
    "Start specified MCHEM scenario as soon as possible"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(rf_scenario_start, self).get_parser(prog_name)
        parser.add_argument('scenario_id', type=int, help='4 digit ID of the scenario')
        parser.add_argument('-m', '--radio_map', dest='radio_map', help='Json file that maps nodes in the scenario to SRN IDs.'
                                                        'All nodes must be assigned. '
                                                        'Assign unused nodes to "None"')
        parser.set_defaults(radio_map=None)
        parser.add_argument('-c', '--cycle', dest='cycle', action='store_true', help='Repeat scenario after it completes')
        parser.set_defaults(cycle=False)
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
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_START,
            con.CLI_SCEN_ID_KEY: parsed_args.scenario_id,
            con.CLI_SCEN_CYCLE_KEY: parsed_args.cycle
        }

        if parsed_args.radio_map is not None:
            # Check the radio map
            try:
                radio_map_str = open(parsed_args.radio_map).read()
                radio_map = json.loads(radio_map_str)
            except:
                msg = "Failed to open json file " + parsed_args.radio_map
                print(msg)
                return
            try:
                check_radio_map(radio_map)
            except ValueError as err:
                msg = "Failed to read json file"
                print(msg)
                return
            # Add the radio map to the json
            data_sent[con.CLI_SCEN_RADIO_MAP_KEY] = radio_map

        ret = connect_and_send(data_sent)
        if ret["status"] == 100:
            scenario_loading = True
            while scenario_loading == True:
                try:
                    # Check the scenario status until it returns a time
                    time.sleep(1)
                    data_sent = {
                        con.CLI_VER_KEY: con.CLI_MSG_VERSION,
                        con.CLI_CMD_KEY: con.CLI_CMD_SCEN_INFO
                    }
                    ret = connect_and_send(data_sent)
                    if ret["status"] == 200:
                        data = json.loads(ret["data"])
                        if data["scenario_status"] in con.MCHEM_SCEN_START_FAIL_STATES:
                            # Failure Higher up
                            msg = "Colosseum failed to schedule the scenario at the Scenario Conductor"
                            print(msg)
                            scenario_loading = False
                        elif data["scenario_start_time"] != None:
                            # Successa
                            t =  datetime.datetime.fromtimestamp(int(data["scenario_start_time"])).strftime("%H:%M:%S")
                            msg = "Scenario Start Time is " + t
                            print(msg)
                            scenario_loading = False
                    elif ret["status"] == 400:
                        msg = ret["message"]
                        print(msg)
                except KeyboardInterrupt:
                    scenario_loading = False
                    pass
        else:
            msg = "Colosseum failed to schedule the scenario at the Resource Manager"
            print(msg)
            print(ret["message"])

        self.log.debug('completed scenario start')


class rf_scenario_stop(Command):
    "Stop the active MCHEM scenario"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('stopping scenario')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_STOP
        }

        ret = connect_and_send(data_sent)
        if ret["status"] == 200:
            print("RF Stop command has been successfully sent")
            print("Waiting for the RF to clear the emulator - This sometimes takes a while")
            print("Check rf info for more information")

        self.log.debug('completed scenario stop')


class rf_scenario_info(ShowOne):
    "Information on the active MCHEM scenario."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('getting active RF scenario info')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_INFO
        }

        ret = connect_and_send(data_sent)
        if ret["status"] == 200:
            data = json.loads(ret["data"])
            rows = (con.MCHEM_SCEN_ID_KEY,
                    con.MCHEM_SCEN_STATUS_KEY,
                    con.MCHEM_SCEN_STARTTIME_KEY,
                    con.MCHEM_SCEN_CYCLE_KEY,
                    "Number of Nodes"
                    )
            if len(data) == 0:
                values = ("", "", "", "", "")
            else:
                values = (str(data[con.MCHEM_SCEN_ID_KEY]),
                    data[con.MCHEM_SCEN_STATUS_KEY],
                    datetime.datetime.fromtimestamp(int(data[con.MCHEM_SCEN_STARTTIME_KEY])).strftime("%H:%M:%S"),
                    data[con.MCHEM_SCEN_CYCLE_KEY],
                    str(len(data[con.MCHEM_SCEN_RADIO_MAP_KEY]))
                    )
            self.log.debug('completed scenario info')
        else:
            print(ret["message"])
            rows = ()
            values = ()

        return(rows, values)

class rf_scenario_radio_map(Lister):
    "Return the current Radio Map."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('getting active radio map')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_INFO
        }

        ret = connect_and_send(data_sent)
        if ret["status"] == 200:
            data = json.loads(ret["data"])
            radio_map = data[con.MCHEM_SCEN_RADIO_MAP_KEY]
            node_list = []

            for i in range(len(radio_map)):
                radio = "Node " + str(i + 1)
                if radio_map[radio] != "None":
                    node = (radio, radio_map[radio]["SRN"], radio_map[radio]["RadioA"], radio_map[radio]["RadioB"])
                else:
                    node = (radio, "None", 0, 0)
                node_list.append(node)
            nodes = tuple(node_list)

            self.log.debug('completed scenario info')

        else:
            print("Error getting Radio Map. Code: " + str(ret["status"]))
            nodes = ()

        return (("Node", "SRN", "RadioA", "RadioB"),
                nodes)


class rf_scenario_list(Lister):
    "List available MCHEM scenarios."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        #self.log.info('getting RF scenario list')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_LIST
        }

        ret = connect_and_send(data_sent)
        if ret['status'] == 200:
            data_rx = json.loads(ret['data'])
            #self.log.info(data_rx)
            scenarios_list = []
            for scenario_dict in data_rx:
                title = "None"
                if "title" in scenario_dict:
                    title = scenario_dict["title"]
                cfreq = "Unset"
                if "center_freq" in scenario_dict:
                    cfreq = scenario_dict["center_freq"]

                scenario_tup = (scenario_dict["scenario_id"],
                                title,
                                len(scenario_dict["radio_resources"]),
                                cfreq,
                                scenario_dict["scenario_cycle_compatible"]
                                )
                scenarios_list.append(scenario_tup)
            scenarios = tuple(scenarios_list)
            #self.log.info('completed scenario list')
        else:
            print("Failed to get the scenario list. Code: " + str(ret['status']))
            print(ret["message"])
            scenarios = ()

        print("For more information the listed scenarios use the link below:\n")
        print(con.WIKI_SCENARIO_LIST)
        print("\n")

        return (("Scenario ID", "Title", "Number of Nodes", "Center Frequency", "Cyclable"), scenarios)

class rf_scenario_list_nodes(Lister):
    "List nodes and radios on a specific scenario."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(rf_scenario_list_nodes, self).get_parser(prog_name)
        parser.add_argument('scenario_id', type=int, help='4 digit ID of the scenario')
        return parser

    def take_action(self, parsed_args):
        """
        Create json message to start a message
        :param parsed_args:
        :return:
        """
        self.log.debug('getting scenario node list')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_SCEN_LIST
        }

        ret = connect_and_send(data_sent)
        if ret['status'] == 200:
            data_rx = json.loads(ret['data'])
            node_list = []
            for scenario in data_rx:
                if scenario["scenario_id"] == parsed_args.scenario_id:
                    radio_resources = scenario["radio_resources"]
                    for i in range(len(radio_resources)):
                        node_id = "NODE " + str(i + 1)
                        node = (node_id, radio_resources[node_id])
                        node_list.append(node)
                    break

            nodes = tuple(node_list)
            self.log.debug('completed scenario list')
        else:
            print("Failed to get the scenario list. Code: " + ret['status'])
            print(ret["message"])
            nodes = ()

        return (("Node", "Number of Antennas"), nodes)

def check_radio_map(user_radio_map):
    """
    Converts the user radio map to the MCHEM
    :param user_radio_map:
    :return:
    """
    for key in user_radio_map:
        if 'Node ' not in key:
            msg = "Json file has bad key " + key
            print(msg)
            raise ValueError(msg)

        if user_radio_map[key] == 'None':
            continue

        required_keys = ["SRN", "RadioA", "RadioB"]
        for rk in required_keys:
            if rk not in user_radio_map[key]:
                print("Bad " + key + " values: " + str(user_radio_map[key]))
                print("Both radios need to be specified on the SRN")
                print("Value for SRN radios must in following format (example Node 5, SRN 3):")
                print('"Node 5": {"SRN": 3, "RadioA": 1, "RadioB": 2}')
                print("Example is for SRN 12")
                raise ValueError
