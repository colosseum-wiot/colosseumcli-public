import logging
import os
import subprocess
import time
from cliff.command import Command
from colosseum_cli import colosseum_cli_constants as con
from colosseum_cli.colosseum_socket import connect_and_send
from cliff.show import ShowOne
from cliff.lister import Lister

#
# Start gps consumer on container
#
class gps_start(Command):
    "Start GPS feed."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(gps_start, self).get_parser(prog_name)
        parser.add_argument('scenario_id', type=int, help='ID of gps scenario (same ID as RF scenario)')
        parser.add_argument('node_id', type=int, help='nodeid of the node\'s gps track to use (refer to the RF '
                                                      'scenario descriptions on pbworks to find the right nodeid)')
        return parser

    def take_action(self, parsed_args):
        self.log.debug("container received gps start command")

        self.log.debug("starting socat/unix socket (step 1 of 3)")
        socket_path = 'UNIX-LISTEN:' + con.CLI_CMD_GPS_UNIX_SOCKET
        process_socat = subprocess.Popen(['socat', socket_path, 'UDP4-SENDTO:127.0.0.1:5900'],
                                         shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # hard wait of 1 second to let the UNIX socket settle
        # TODO: find a better way of checking the creation of the UNIX socket
        time.sleep(1)

        self.log.debug("setting permission on gps unix socket (step 2 of 3)")
        # give the UNIX socket 777 permissions; this gives the baremetal access to this UNIX socket
        os.chmod(con.CLI_CMD_GPS_UNIX_SOCKET, 0o777)

        self.log.debug("starting gpsd (step 3 of 3)")
        # note: since the srn's gps feeder hasn't started yet, the container's gpsd will be active but won't
        # produce any GPS coordinates
        process_gpsd = subprocess.Popen(['gpsd', 'udp://127.0.0.1:5900', '-n', '-N', '-S', '6000'],
                                        shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # send 'gps start' message to srn; which will start the gps feed from baremetal
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_GPS_START,
            con.CLI_CMD_GPS_RFID_KEY: parsed_args.scenario_id,
            con.CLI_CMD_GPS_NODEID_KEY: parsed_args.node_id
        }
        ret = connect_and_send(data_sent)

        if ret["status"] == con.CLI_RET_CODE_SUCCESS:
            self.log.debug("gps processes on srn started")
            print("\nGPS started. To check the gps feed in the container, run \'cgps 127.0.0.1:6000\'\n")
        else:
            self.log.error("gps processes on srn failed to start")


#
# Stop gps consumer on container
#
class gps_stop(Command):
    "Stop GPS feed."

    log = logging.getLogger(__name__)

    #def get_parser(self, prog_name):
    #    parser = super(gps_start, self).get_parser(prog_name)
    #    parser.add_argument('filename', type=str, help='Name of the NMEA CSV input file.')
    #    return parser

    def take_action(self, parsed_args):
        self.log.debug("container received gps stop command")

        # TODO: figure out a better/smarter way of killing the gpsd processes
        # the way the gpsd daemon is stopped is by issuing a "pkill -f" call. Which to say the least, is such a bad
        # way of doing things. The proper way would be to use the multiprocessing library to keep track of the
        # gps spawned processes from gps_start. Then issue a sigterm message to each process to gracefully shut it down.

        self.log.debug("stopping gpsd (step 1 of 2)")
        process1 = subprocess.Popen(['pkill', '-f', 'gpsd'],
                                    shell=False)

        self.log.debug("stopping socat/unix-socket (step 2 of 2)")
        process3 = subprocess.Popen(['pkill', '-f', 'socat'],
                                    shell=False)

        self.log.debug("all gps processes on container stopped")

        # send 'gps stop' message to srn; which will stop the gps feed from baremetal
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_GPS_STOP
        }
        ret = connect_and_send(data_sent)

        if ret["status"] == con.CLI_RET_CODE_SUCCESS:
            self.log.debug("gps processes on srn stopped")
            print("\nGPS stopped\n")
        else:
            self.log.error("gps processes on srn failed to stop")

#
# Show gps scenario list on container
#
class gps_scenario_list(Command):
    "List GPS scenarios."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        print("\nThe GPS scenario id is the same as the RF scenario id (rf scenario list)\n")

#
# Get GPS scenario
#
class gps_info(Command):
    "Information on the active GPS scenario."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):

        self.log.debug('getting active GPS info')
        data_sent = {
            con.CLI_VER_KEY: con.CLI_MSG_VERSION,
            con.CLI_CMD_KEY: con.CLI_CMD_GPS_INFO
        }

        ret = connect_and_send(data_sent)

        if ret["status"] == con.CLI_RET_CODE_SUCCESS:
            data = ret["data"]
            gps_rf_scenario_id = data[con.CLI_CMD_GPS_RFID_KEY]
            gps_rf_node_id = data[con.CLI_CMD_GPS_NODEID_KEY]

            if (gps_rf_scenario_id is None) and (gps_rf_node_id is None):
                print("\nGPS is currently not running\n")
            else:
                print("\nGPS is currently running with RF scenario id " + str(gps_rf_scenario_id) +
                      " and RF node id " + str(gps_rf_node_id) + "\n")
