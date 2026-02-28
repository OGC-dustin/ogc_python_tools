# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Python3 CAN Listener - On-device diagnostic tools to monitor/log CAN traffic
#
# 0.0.0 DK proof of concept, basic CAN listening loop ( hard coded to vcan0 )
# 0.1.0 DK added command line parsing with options for help printout and log file target
# 0.2.0 DK added command line parsing options for CAN interface and channel
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '0.2.0'
__author__ = 'dustin ( at ) ogc.engineering'

import getopt
import sys
import can
import time
import ogc_python_logging as l

# --------------------------------------------------------------------------------------------------------------- splash
# https://patorjk.com/software/taag/#p=display&f=Big&t=OGC+CAN+Listener&x=none&v=4&h=4&w=80&we=false
# ----------------------------------------------------------------------------------------------------------------------
splash = r"""
   ____   _____  _____    _____          _   _   _      _     _
  / __ \ / ____|/ ____|  / ____|   /\   | \ | | | |    (_)   | |
 | |  | | |  __| |      | |       /  \  |  \| | | |     _ ___| |_ ___ _ __   ___ _ __
 | |  | | | |_ | |      | |      / /\ \ | . ` | | |    | / __| __/ _ \ '_ \ / _ \ '__|
 | |__| | |__| | |____  | |____ / ____ \| |\  | | |____| \__ \ ||  __/ | | |  __/ |
  \____/ \_____|\_____|  \_____/_/    \_\_| \_| |______|_|___/\__\___|_| |_|\___|_|
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

class Listener( can.Listener ):
    def on_message_received( self, msg: can.Message ) -> None:
        """Called whenever a new message arrives on the bus."""
        l.log( l.INFO, f"Received CAN ID: {msg.arbitration_id:#x} data: {msg.data} raw: {msg}" )

    def on_error( self, exc: Exception ) -> None:
        """Called if an error occurs in the receive thread."""
        l.log( l.ERROR, f"Error in listener: {exc}" )

def notifier_listener_example():
    try:
        with can.Bus( interface = arguments.interface, channel = arguments.channel, receive_own_messages = True ) as bus:
            l.log( l.NOTICE, f"Listening on {bus.channel_info} with Notifier..." )

            # Create listener instances
            listener = Listener()

            # The Notifier uses a separate thread to read from the bus
            notifier = can.Notifier(bus, [listener], timeout=1.0)

            try:
                while ( True ):
                    pass
            except KeyboardInterrupt:
                notifier.stop()
                l.log( l.NOTICE, "Exiting due to keyboard interrupt - Notifier stopped" )
                exit()
    except OSError as e:
        l.log( l.FATAL, f"Exception caught while attempting to open CAN bus: {e}" )
    except Exception as e:
        l.log( l.FATAL, f"Unhandled exception in CAN bus listener: {e}" )
    finally:
        exit()

# ----------------------------------------------------------------------------------------------------------------- help
#
# ----------------------------------------------------------------------------------------------------------------------
help_text = """
-h	       : Print this help message
-f --file      : Set path for log file
-i --interface : Set CAN interface ( socketcan, kvaser )
-c --channel   : Set CAN channel ( vcan0, can0, 0 )
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
                                    'hf:i:c:',
                                    [ 'help',
                                      'file=',
                                      'interface=',
                                      'channel='
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
            else:
                l.log( l.ERROR, f"unknown command line option/arg: {opt}/{arg}" )
    except getopt.GetoptError:
        print_help()
        sys.exit( 1 )

    notifier_listener_example()
