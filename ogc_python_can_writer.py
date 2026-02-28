# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Python3 CAN Writer - On-device diagnostic tools to write/log CAN message(s)
#
# 0.0.0 DK proof of concept, hard coded single shot CAN writer
# 0.1.0 DK add command line argument handling for CAN interface, channel, and basic message contents
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '0.1.0'
__author__ = 'dustin ( at ) ogc.engineering'

import getopt
import sys
import ast
import can
import time
import ogc_python_logging as l

# --------------------------------------------------------------------------------------------------------------- splash
# https://patorjk.com/software/taag/#p=display&f=Big&t=OGC+CAN+Writer&x=none&v=4&h=4&w=80&we=false
# ----------------------------------------------------------------------------------------------------------------------
splash = r"""
   ____   _____  _____    _____          _   _  __          __   _ _
  / __ \ / ____|/ ____|  / ____|   /\   | \ | | \ \        / /  (_) |
 | |  | | |  __| |      | |       /  \  |  \| |  \ \  /\  / / __ _| |_ ___ _ __
 | |  | | | |_ | |      | |      / /\ \ | . ` |   \ \/  \/ / '__| | __/ _ \ '__|
 | |__| | |__| | |____  | |____ / ____ \| |\  |    \  /\  /| |  | | ||  __/ |
  \____/ \_____|\_____|  \_____/_/    \_\_| \_|     \/  \/ |_|  |_|\__\___|_|
"""
def print_splash( run_path ):
    print ( "-" * 80 )
    print ( splash )
    print ( run_path )
    print ( f"Version: {__version__} - {__author__}" )
    print ( "-" * 80 )

# ---------------------------------------------------------------------------------------------------------- CAN Helpers
#
# ----------------------------------------------------------------------------------------------------------------------
class arguments:
    interface = "socketcan"
    channel = "vcan0"
    extended_id_flag = False
    arbitration_id = 0x123
    data = [ 1, 2, 3, 4, 5, 6, 7, 8 ]

def writer_example():
    with can.Bus( interface = arguments.interface, channel = arguments.channel, receive_own_messages = True ) as bus:
        log_data_string = '[{}]'.format(', '.join( f"0x{x:x}" for x in arguments.data ) )
        l.log( l.NOTICE, f"Writing extended flag:{ arguments.extended_id_flag }, ID:{ hex( arguments.arbitration_id ) }, data:{ log_data_string } to { bus.channel_info } with Writer..." )

        # Send a message to demonstrate reception (receive_own_messages=True required)
        msg = can.Message( arbitration_id=arguments.arbitration_id,
                           data=arguments.data,
                           is_extended_id=arguments.extended_id_flag
                         )
        bus.send(msg)
        print("Message sent.")

# ----------------------------------------------------------------------------------------------------------------- help
#
# ----------------------------------------------------------------------------------------------------------------------
help_text = """
-h               : FLAG Print this help message
-f --file        : Set path for log file
-i --interface   : Set CAN interface ( socketcan, kvaser )
-c --channel     : Set CAN channel ( vcan0, can0, 0 )
-x --extended    : FLAG use of extended ID flag
-a --arbitration : Set arbitration ID, use hex value 0-9 a-f ( with or without "0x" prefix )
-d --data        : set data list wrapped in brackets, up to 8 hex values i.e. '[0x02, 0x04, 0x06, 0x08, 0xaf, 0x5d]'
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
                                    'hxf:i:c:a:d:',
                                    [ 'help',
                                      'extended',
                                      'file=',
                                      'interface=',
                                      'channel=',
                                      'arbitration=',
                                      'data='
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
                # TODO: add handling of numeric versus string channels ( issues seen in Windows use )
                arguments.channel = arg
            elif opt in ( '-x', '--extended' ):
                arguments.extended_id_flag = True
            elif opt in ( '-a', '--arbitration' ):
                arguments.arbitration_id = int( arg, 16 )
            elif opt in ( '-d', '--data' ):
                arguments.data = ast.literal_eval( arg )
            else:
                l.log( l.ERROR, f"unknown command line option/arg: {opt}/{arg}" )
    except getopt.GetoptError:
        print_help()
        sys.exit( 1 )

    writer_example()
