# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Python3 CANopen Reader - Reads .eds file to query a CANopen device
#
# 0.0.0 DK proof of concept, edit/read CANopen device values based on .eds descriptions
# 0.1.0 DK added command line handling for logging, CAN, and CANopen settings
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '0.2.0'
__author__ = 'dustin ( at ) ogc.engineering'

import getopt
import sys
import canopen
import time
import ogc_python_logging as l

# --------------------------------------------------------------------------------------------------------------- splash
# https://patorjk.com/software/taag/#p=display&f=Big&t=OGC+CANopen+Reader&x=none&v=4&h=4&w=80&we=false
# ----------------------------------------------------------------------------------------------------------------------
splash = r"""
   ____   _____  _____    _____          _   _                          _____                _
  / __ \ / ____|/ ____|  / ____|   /\   | \ | |                        |  __ \              | |
 | |  | | |  __| |      | |       /  \  |  \| | ___  _ __   ___ _ __   | |__) |___  __ _  __| | ___ _ __
 | |  | | | |_ | |      | |      / /\ \ | . ` |/ _ \| '_ \ / _ \ '_ \  |  _  // _ \/ _` |/ _` |/ _ \ '__|
 | |__| | |__| | |____  | |____ / ____ \| |\  | (_) | |_) |  __/ | | | | | \ \  __/ (_| | (_| |  __/ |
  \____/ \_____|\_____|  \_____/_/    \_\_| \_|\___/| .__/ \___|_| |_| |_|  \_\___|\__,_|\__,_|\___|_|
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

    # Start with creating a network representing one CAN bus
    network = canopen.Network()

    # Add a remote node with a corresponding Object Dictionary (EDS file)
    # Replace 6 with your node's ID and '/path/to/object_dictionary.eds' with your EDS file path
    node = canopen.RemoteNode( arguments.node_number, arguments.eds_path )
    network.add_node( node )

    try:
        # Connect to the CAN bus
        # The arguments are passed to python-can's can.Bus() constructor
        # Example using socketcan on Linux:
        network.connect( interface = arguments.interface, channel = arguments.channel )
        # For other interfaces like Kvaser, PCAN, etc., see the python-can documentation
        # network.connect(interface='kvaser', channel=0, bitrate=250000)

        # Wait for the node to become operational (optional, but good practice)
#        node.nmt.wait_for_bootup(10)
#        l.log( l.INFO, f"Node { node.id } is online and state is { node.nmt.state }" )

        # --- SDO Communication Examples ---

        # Read a variable using SDO (using object name or index/subindex)
        device_name = node.sdo['Manufacturer device name'].raw
        vendor_id = node.sdo[0x1018][1].raw
        l.log( l.INFO, f'Device Name: { device_name }' )
        l.log( l.INFO, f'Vendor ID: { vendor_id }' )

        # Write a variable using SDO
        # node.sdo['Producer heartbeat time'].raw = 1000  # Set heartbeat time to 1 second

        # --- PDO Communication Examples (requires node to be in OPERATIONAL state) ---

        # Set the node to OPERATIONAL state
        # node.nmt.state = 'OPERATIONAL' # This might not be necessary if already operational after bootup

        # Example of accessing a PDO variable (must be mapped in the EDS or dynamically remapped)
        # actual_speed = node.rpdo['Velocity actual value'].raw
        # l.log( l.INFO, f'Actual speed: { actual_speed }' )

    except Exception as e:
        l.log( l.ERROR, f"An error occurred: { e }" )

    finally:
        # Disconnect from the CAN bus when done
        network.disconnect()
