# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Custom Python 3 Logging Library - Threshold and format log entries to console, file, and queue for application use
#
# V1.0 - PC use with console, file and queue operations in place
#
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '1.0.0'
__author__ = 'dustin ( at ) ogc.engineering'

import datetime
import queue
import os

# ----------------------------------------------------------------------------------------------------------------------
# Level definitions and library resources
# ----------------------------------------------------------------------------------------------------------------------

FATAL = 0
ERROR = 1
WARNING = 2
NOTICE = 3
INFO = 4
DEBUG = 5
TRACE = 6

LEVEL_STRING = [ "FATAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG", "TRACE" ]

class settings:
    level_threshold = INFO
    flag_verbosity_override = False
    flag_storage_use = False
    storage = queue.Queue( maxsize = 0 ) # 0 = infinite size
    file = "" # used to track file usage

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def threshold_get():
    return ( settings.level_threshold )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def threshold_set( state ):
    if ( ( TRACE >= state ) and ( FATAL <= state ) ):
        settings.level_threshold = state
        return ( True )
    else:
        return ( False )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def verbosity_overide_get():
    return ( settings.flag_verbosity_override )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def verbosity_override_set( state ):
    if ( ( True == state ) or ( False == state ) ):
        settings.flag_verbosity_override = state
        return ( True )
    else:
        return ( False )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def storage_use_get():
    return ( settings.flag_storage_use )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def storage_use_set( state ):
    if ( ( True == state ) or ( False == state ) ):
        settings.flag_storage_use = state
        if ( False == state ):
            while( False == settings.storage.empty() ):
                storage_pop() # clear the queue if we turned off storage use
        return ( True )
    else:
        return ( False )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def storage_is_empty():
    return ( settings.storage.empty() )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def storage_push( string ):
    settings.storage.put( string.rstrip() )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def storage_pop():
    if ( False == settings.storage.empty() ):
        return ( settings.storage.get().rstrip() )
    else:
        return ( "" )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def log_file_get():
    return ( settings.file )

# ----------------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
def log_file_set( path ):
    settings.file = path

# ----------------------------------------------------------------------------------------------------------------------
#                                                                                                      Main logging call
# Returns:
#     Boolean - Success of logging process
# Inputs:
#     Enumeration - level ( FATAL, ERROR, WARNING, NOTICE, INFO, DEBUG, TRACE )
#     string - string to be logged
# ----------------------------------------------------------------------------------------------------------------------
def log( level, string ):
    # test thresholding
    if ( ( True == settings.flag_verbosity_override ) or ( level <= settings.level_threshold ) ):
        now = datetime.datetime.now()
        temp = "%10s | %s | %s\n" % ( LEVEL_STRING[ level ], now.strftime( "%Y%m%d %H:%M:%S.%f" ), string.rstrip() )
        print( temp.rstrip(), flush = True )
        if ( True == settings.flag_storage_use ):
            storage_push( temp )
        if ( settings.file != "" ):
            try:
                f = open( settings.file, "a" )
                f.write( temp )
                f.close()
            except IOError as err1:
                try:
                    f = open( settings.file, "w" )
                    f.write( temp )
                    f.close()
                except IOError as err2:
                    temp2 = "logging failed to open file %s" % ( settings.file )
                    settings.file = ""
                    log( ERROR, temp2 )
                    return ( False )
        return ( True )
    else:
        return ( False )

# ----------------------------------------------------------------------------------------------------------------------
#                                                                                                           Unit Testing
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    error_count = 0

    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "OGC.Engineering - Python logging library unit testing ( STARTING )" )
    log( NOTICE, "--------------------------------------------------------------------------------" )

    # test thresholding ( using return value of False to logging event )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "TEST - thresholding" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    ret_val = log( TRACE, "testing TRACE level thresholding" )
    if ( False == ret_val ):
        log( INFO, "PASSED" )
    else:
        error_count += 1
        log( ERROR, "FAILED - log threshold returned unexpected value (%r)", ret_val )

    # test verbosity override ( set override and retry log above threshold level )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "TEST - verbosity override" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    verbosity_override_set( True )
    ret_val = log( TRACE, "testing TRACE level with verbosity override" )
    if ( True == ret_val ):
        log( INFO, "PASSED" )
    else:
        error_count += 1
        log( ERROR, "FAILED - log after verbosity override returned unexpected value (%r)", ret_val )

    # test storage to file
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "TEST - storage to file" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log_file_set( "unit_test.log" ) # a temporary log file to be erased
    log( DEBUG, "testing log to file" )
    log_file_size = os.path.getsize( log_file_get() )
    if ( log_file_size == 60 ):
        log( INFO, "PASSED" )
    else:
        error_count += 1
        log( ERROR, "FAILED with recorded size of (%u)" % ( log_file_size ) )
    os.remove( settings.file )
    settings.file = ""
    # test storage to queue push, pop, and empty testing pre/post turn off of storage
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "TEST - storage to queue" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    sub_error_count = error_count
    ret_val = storage_is_empty()
    if ( False == ret_val ): # storage should be empty
        error_count += 1
        log( ERROR, "FAILED - storage should have been empty before starting storage queue test" )
        while ( False == storage_is_empty() ):
            storage_pop()
    storage_use_set( True ) # set storage use flag
    log( DEBUG, "storage use test message, pushed to queue in log() call" ) # push a message
    ret_val = storage_is_empty()
    if ( True == ret_val ): # storage should NOT be empty
        error_count += 1
        log( ERROR, "FAILED - storage should have NOT been empty after turning on storage use and logging a message" )
    temp_message = storage_pop() # pop a message
    ret_val = storage_is_empty()
    log( INFO, "message popped from storage (%s)" % ( temp_message ) )
    if ( False == ret_val ): # storage should be empty
        error_count += 1
        log( ERROR, "FAILED - storage should have been empty after poping only message" )
        while ( False == storage_is_empty() ):
            storage_pop()
    ret_val = storage_is_empty()
    if ( True == ret_val ): # storage should NOT be empty
        error_count += 1
        log( ERROR, "FAILED - storage should have NOT been empty after pushing multiple messages" )
    log( INFO, "turning off storage, this message is the last message to be pushed into queue" )
    storage_use_set( False ) # turn off storage ( which should clear the queue
    ret_val = storage_is_empty()
    if ( False == ret_val ): # storage should be empty
        error_count += 1
        log( ERROR, "FAILED - storage should have been empty after turning off storage use" )
        while ( False == storage_is_empty() ):
            storage_pop()
    if ( error_count == sub_error_count ):
        log( INFO, "PASSED" )
    else:
        log( ERROR, "FAILED - error count increased during this multipart test" )

    # while override is set, print all types for example/user approval
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "TEST - printing out all types, please review formatting manually" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( TRACE, "example TRACE message" )
    log( DEBUG, "example DEBUG message" )
    log( INFO, "example INFO message" )
    log( NOTICE, "example NOTICE message" )
    log( WARNING, "example WARNING message" )
    log( ERROR, "example ERROR message" )
    log( FATAL, "example FATAL message" )

    log( NOTICE, "--------------------------------------------------------------------------------" )
    log( INFO, "OGC.Engineering - Python logging library unit testing ( ENDING )" )
    if ( error_count > 0 ):
        log( ERROR, "FAILED with error_count (%u)" % ( error_count ) )
    else:
        log( INFO, "PASSED" )
    log( NOTICE, "--------------------------------------------------------------------------------" )
