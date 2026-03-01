# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Python3 CANopen Device Simulator - Reads .eds file to simulate CANopen device
#
# 0.0.0 DK proof of concept, hosting CANopen device on vcan0
# 0.1.0 DK add command line handling for logging, CAN, and CANopen settings
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '0.1.0'
__author__ = 'dustin ( at ) ogc.engineering'

import getopt
import sys
import canopen
import time
import ogc_python_logging as l

# --------------------------------------------------------------------------------------------------------------- splash
# https://patorjk.com/software/taag/#p=display&f=Big&t=OGC+CANopen+Device+Sim&x=none&v=4&h=4&w=80&we=false
# ----------------------------------------------------------------------------------------------------------------------
splash = r"""
   ____   _____  _____    _____          _   _                          _____             _             _____ _
  / __ \ / ____|/ ____|  / ____|   /\   | \ | |                        |  __ \           (_)           / ____(_)
 | |  | | |  __| |      | |       /  \  |  \| | ___  _ __   ___ _ __   | |  | | _____   ___  ___ ___  | (___  _ _ __ ___
 | |  | | | |_ | |      | |      / /\ \ | . ` |/ _ \| '_ \ / _ \ '_ \  | |  | |/ _ \ \ / / |/ __/ _ \  \___ \| | '_ ` _ \
 | |__| | |__| | |____  | |____ / ____ \| |\  | (_) | |_) |  __/ | | | | |__| |  __/\ V /| | (_|  __/  ____) | | | | | | |
  \____/ \_____|\_____|  \_____/_/    \_\_| \_|\___/| .__/ \___|_| |_| |_____/ \___| \_/ |_|\___\___| |_____/|_|_| |_| |_|
                                                    | |
                                                    |_|
"""
def print_splash( run_path ):
    print ( "-" * 80 )
    print ( splash )
    print ( run_path )
    print ( f"Version: {__version__} - {__author__}" )
    print ( "press CTRL-C to quit" )
    print ( "-" * 80 )

# ---------------------------------------------------------------------------------------------------------- CAN Helpers
#
# ----------------------------------------------------------------------------------------------------------------------
class arguments:
    interface = "socketcan"
    channel = "vcan0"
    node_number = 5
    eds_path = "example_canopen_node.eds"

# ----------------------------------------------------------------------------------------------------------------- help
#
# ----------------------------------------------------------------------------------------------------------------------
help_text = """
-h             : Print this help message
-f --file      : Set path for log file
-i --interface : Set CAN interface ( socketcan, kvaser )
-c --channel   : Set CAN channel ( vcan0, can0, 0 )
-n --node      : Set CANopen node ID ( i.e. 5 )
-p --path      : Set CANopen eds file path ( i.e. example_canopen_node.eds )
"""
def print_help():
    print( "help help help help help help help help help help help help help help help help" )
    print( help_text )
    print( "help help help help help help help help help help help help help help help help" )

# ----------------------------------------------------------------------------------------------------------------- main
#
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    l.verbosity_override_set( True ) # we want to see ALL the logs
    print_splash( sys.argv[ 0 ] )

    try:
        opts, args = getopt.getopt( sys.argv[ 1: ],
                                    'hf:i:c:n:p:',
                                    [ 'help',
                                      'file=',
                                      'interface=',
                                      'channel=',
                                      'node=',
                                      'path='
                                    ] )
        for opt, arg in opts:
            if opt in ( '-h', '--help' ):
                print_help()
                sys.exit( 0 )
            elif opt in ( '-f', '--file' ):
                l.log( l.NOTICE, f"Setting logfile location to: {arg}" )
                l.log_file_set( arg )
            elif opt in ( '-i', '--interface' ):
                arguments.interface = arg
            elif opt in ( '-c', '--channel' ):
                # TODO: add handling of numeric versus string channels ( issues seen in Windows use of "0" )
                arguments.channel = arg
            elif opt in ( '-n', '--node' ):
                arguments.node_number = int( arg )
            elif opt in ( '-p', '--path' ):
                arguments.eds_path = arg
            else:
                l.log( l.ERROR, f"unknown command line option/arg: {opt}/{arg}" )
    except getopt.GetoptError:
        print_help()
        sys.exit( 1 )

    # Create a network representing the CAN bus
    network = canopen.Network()
    # Connect to the virtual CAN interface vcan0
    network.connect( interface = arguments.interface, channel = arguments.channel )

    # Create a local node (simulated device) on the network
    # This node will use the definitions from the EDS file
    try:
        local_node = network.create_node( arguments.node_number, arguments.eds_path )
        l.log( l.INFO, f"Local node { arguments.node_number } created successfully with { arguments.eds_path }" )
    except Exception as e:
        l.log( l.ERROR, f"Failed creating local node: { e }" )
        # Handle cases where the EDS file might be invalid or missing
        exit()

    # Example: Modify an object dictionary entry defined in your EDS file
    # Replace 'Your_Object_Name' or the index with actual entries in your EDS
    try:
        # Access an object by name (if defined in EDS)
        local_node.sdo[ 0x3050 ][ 0x00 ].phys = 123
        l.log( l.INFO, f"Set object 0x3050:00 to 123" )

        # Continuously run the network to process messages
        l.log( l.INFO, f"Local node running simulating CANopen device ( CTRL-C to exit )" )
        while True:
            # The local node automatically handles SDO and some basic services
            time.sleep( 0.1 )

    except KeyError:
        l.log( l.ERROR, "Object not found in the EDS file" )
    except KeyboardInterrupt:
        # Disconnect from the network on exit
        network.disconnect()
