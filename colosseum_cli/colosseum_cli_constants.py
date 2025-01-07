"""
Competitor CLI Constants
"""
CLI_APP_VERION = '19.0.0'
CLI_MSG_VERSION = '3.0'

SOCKET_PATH = '/socket/clisocket'
TEST_SOCKET_PATH = '/tmp/socket/'
TEST_SOCKET = TEST_SOCKET_PATH + 'clisocket'

CLI_TEST_MODE_ENV = 'COLOSSEMCLI_TEST_MODE'

#Sending Json keys
CLI_CMD_KEY = "command"
CLI_VER_KEY = "version"
CLI_SNAPSHOT_FILE_KEY = "filename"
CLI_SNAPSHOT_PATH_KEY = "path"
CLI_SCEN_ID_KEY = "scenario_id"
CLI_SCEN_RADIO_MAP_KEY = "srn_radio_mapping"
CLI_SCEN_CYCLE_KEY = "scenario_cycle"

#Sending Json values
CLI_CMD_CTNR_SNAPSHOT = "snapshot"
CLI_CMD_SCEN_START = "rf_scenario_start"
CLI_CMD_SCEN_STOP = "rf_scenario_stop"
CLI_CMD_SCEN_INFO = "rf_scenario_info"
CLI_CMD_SCEN_LIST = "rf_scenario_list"
CLI_CMD_TGEN_START = "tgen_start"
CLI_CMD_TGEN_STOP = "tgen_stop"
CLI_CMD_TGEN_INFO = "tgen_info"
CLI_CMD_TGEN_LIST = "tgen_list"
CLI_SNAPSHOT_PATH = ""

CLI_CMD_GPS_START = "gps_start"
CLI_CMD_GPS_STOP = "gps_stop"
CLI_CMD_GPS_SCEN_LIST = "gps_scenario_list"
CLI_CMD_GPS_INFO = "gps_info"
CLI_CMD_GPS_UNIX_SOCKET = "/socket/gpssocket"
CLI_CMD_GPS_RFID_KEY = "gps_rfid"
CLI_CMD_GPS_NODEID_KEY = "gps_nodeid"

MCHEM_SCEN_STOP_COMPLETE_STATES = ['CLEARED', 'ERROR']
MCHEM_SCEN_STOP_FAIL_STATES = ['ERROR']
MCHEM_SCEN_START_FAIL_STATES = ['COMPLETED', 'ABORTED', 'CLEARED', 'ERROR']
MCHEM_SCEN_RES_ID_KEY = 'reservation_id'
MCHEM_SCEN_COMP_ID_KEY = 'competitor_id'
MCHEM_SCEN_ID_KEY = 'scenario_id'
MCHEM_SCEN_RADIO_MAP_KEY = 'srn_radio_mapping'
MCHEM_SCEN_CYCLE_KEY = 'scenario_cycle'
MCHEM_SCEN_STOP_KEY = 'stop_scenario'
MCHEM_SCEN_STARTTIME_KEY = 'scenario_start_time'
MCHEM_SCEN_STATUS_KEY = 'scenario_status'

#SRN to CLI return codes
CLI_RET_CODE_KEEPALIVE = 100
CLI_RET_CODE_SUCCESS = 200
CLI_RET_CODE_ERROR = 400

#Scenario Website
WIKI_SCENARIO_LIST = 'http://sc2colosseum.pbworks.com/w/page/Scenarios'

#USRP Flashing
CLI_CMD_USRP_INFO = "usrp_info"
CLI_CMD_USRP_FLASH = "usrp_flash"
USRP_FLASH_FILEPATH_KEY = 'filename'
