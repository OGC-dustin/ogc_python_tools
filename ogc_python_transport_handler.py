# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Custom Python 3 Transport Handler - Abstracting socket or serial transport details
# ----------------------------------------------------------------------------------------------------------------------
import socket
import serial
import ogc_python_logging as l

SERIAL = 0
SOCKET = 1

TYPE_TO_STRING = [ "SERIAL", "SOCKET" ]

class settings:
    t_type = SERIAL
    addr_path = "/dev/ttyUSB0"
    port_speed = 115200
    t_file = ""
    buffer_tx = ""
    buffer_rx = ""

# --------------------------------------------------------------------------------------------------- transport_type_get
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_type_get():
    return ( settings.t_type )

# --------------------------------------------------------------------------------------------------- transport_type_set
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_type_set( set_type ):
    if ( ( SERIAL <= set_type ) and ( SOCKET >= set_type ) ):
        if ( settings.t_file != "" ):
            transport_close()
        settings.t_type = set_type

# ---------------------------------------------------------------------------------------------- transport_addr_path_get
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_addr_path_get():
    return ( settings.addr_path )

# ---------------------------------------------------------------------------------------------- transport_addr_path_set
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_addr_path_set( new_path ):
    if ( settings.t_file != "" ):
        transport_close()
    settings.addr_path = new_path

# --------------------------------------------------------------------------------------------- transport_port_speed_get
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_port_speed_get():
    return ( settings.port_speed )

# --------------------------------------------------------------------------------------------- transport_port_speed_set
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_port_speed_set( new_port_speed ):
    if ( settings.t_file != "" ):
        transport_close()
    settings.port_speed = new_port_speed

# ------------------------------------------------------------------------------------------------------- transport_open
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_open():
    if ( settings.t_file == "" ):
        if ( settings.t_type == SERIAL ):
            try:
                settings.t_file = serial.Serial(
                                                settings.addr_path,
                                                baudrate = settings.port_speed,
                                                parity = serial.PARITY_NONE,
                                                stopbits = serial.STOPBITS_ONE,
                                                bytesize = serial.EIGHTBITS,
                                                timeout = 0.5,
                                                rtscts = False,
                                                dsrdtr = False,
                                                xonxoff = False
                                               )
                if ( settings.t_file != "" ):
                    return ( True )
                else:
                    return ( False )
            except Exception as err:
                l.log( l.ERROR, "transport open for SERIAL returned err(%s)" % ( err ) )
                return ( False )
        elif ( settings.t_type == SOCKET ):
            try:
                settings.t_file = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                if ( settings.t_file != "" ):
                    settings.t_file.connect( ( settings.addr_path, settings.port_speed ) )
                    return ( True )
                else:
                    return ( False )
            except Exception as err:
                l.log( l.ERROR, "transport open for SOCKET returned err(%s)" % ( err ) )
                return ( False )
        else:
            l.log( l.ERROR, "unknown type found (%u)" % ( settings.t_type ) )
            return ( False )
    else:
        l.log( l.ERROR, "(%u,%s) file already opened" % ( settings.t_type, TYPE_TO_STRING[ settings.t_type ] ) )
        return ( True )

# ------------------------------------------------------------------------------------------------------ transport_close
#
# ----------------------------------------------------------------------------------------------------------------------
def transport_close():
    if ( settings.t_file != "" ):
        if ( settings.t_type == SERIAL ):
            settings.t_file.close()
            settings.t_file = ""
            l.log( l.TRACE, "SERIAL transport connection closed" )
            return ( True )
        elif ( settings.t_type == SOCKET ):
            settings.t_file.shutdown()
            settings.t_file = ""
            l.log( l.TRACE, "SOCKET transport connection shutdown" )
            return ( True )
        else:
            l.log( l.ERROR, "unknown type found (%u,%s)" % ( settings.t_type ) )
            return ( False )
    else:
        l.log( l.ERROR, "transport file not opened" )
        return ( False )

# -------------------------------------------------------------------------------------------------------- get_length_tx
#
# ----------------------------------------------------------------------------------------------------------------------
def get_length_tx():
    return ( len( settings.buff_tx ) )

# -------------------------------------------------------------------------------------------------------- get_length_rx
#
# ----------------------------------------------------------------------------------------------------------------------
def get_length_rx():
    return ( len( settings.buff_rx ) )

# ------------------------------------------------------------------------------------------------------------- put_char
#
# ----------------------------------------------------------------------------------------------------------------------
def put_char( new_char ):
    settings.buff_tx.append( new_char )

# -------------------------------------------------------------------------------------------------------------- put_str
#
# ----------------------------------------------------------------------------------------------------------------------
def put_str( new_string ):
    settings.buff_tx.extend( new_string )
    
# ------------------------------------------------------------------------------------------------------------- get_char
#
# ----------------------------------------------------------------------------------------------------------------------
def get_char():
    ch = b'/x00'
    if ( len( settings.buff_rx ) > 0 ):
        ch = settings.buff_rx[ 0 : 1 ]
        del settings.buff_rx[ 0 : 1 ]
    return ( ch )

# -------------------------------------------------------------------------------------------------------------- get_str
#
# ----------------------------------------------------------------------------------------------------------------------
def get_str():
    new_string = bytearray()
    if ( len( settings.buff_rx ) > 0 ):
        new_string.extend( settings.buff_rx[ 0 : 1 ] )
        del settings.buff_rx[ 0 : 1 ]
    return ( ch )

# -------------------------------------------------------------------------------------------------------------- service
#
# ----------------------------------------------------------------------------------------------------------------------
def service():
    if ( settings.t_file != "" ):
        if ( settings.t_type == SERIAL ):
            while ( settings.t_file.inWaiting() > 0 ):
                settings.buff_rx += settings.t_file.read( 1 )
            while ( len( settings.buff_tx ) > 0 ):
                settings.t_file.write( settings.buff_tx[ 0 : 1 ] )
                del settings.buff_tx[ 0 : 1 ]
        elif ( settings.t_type == SOCKET ):
            settings.buff_rx += settings.t_file.recv( 1 )
            while ( len( settings.buff_tx ) > 0 ):
                settings.t_file.send( settings.buff_tx[ 0 : 1 ] )
                del settings.buff_tx[ 0 : 1 ]
        else:
            l.log( l.ERROR, "can't service an unknown transport type" )

# ----------------------------------------------------------------------------------------------------------------- main
#
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    error_count = 0

    l.verbosity_override_set( True ) # we want to see ALL the logs for this unit test

    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )
    l.log( l.INFO, "OGC.Engineering - Python transport handler library unit testing ( STARTING )" )
    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )

    if ( False != transport_close() ):
        l.log( l.ERROR, "closing a blank transport returned unexpected result" )

    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )
    l.log( l.INFO, "OGC.Engineering - Python transport handler library unit testing ( ENDING )" )
    if ( error_count > 0 ):
        l.log( l.ERROR, "FAILED with error_count (%u)" % ( error_count ) )
    else:
        l.log( l.INFO, "PASSED" )
    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )

