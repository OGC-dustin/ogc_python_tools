# ----------------------------------------------------------------------------------------------------------------------
# OGC.Engineering
#     Custom Python 3 Textual User Interface Library - Curses Textual Interface Helper
#
# V0.1.0 - Master frame and user input handling ( keyboard and mouse )
#
# ----------------------------------------------------------------------------------------------------------------------
__version__ = '0.1.0'
__author__ = 'dustin ( at ) ogc.engineering'

import ogc_python_logging as l

# ----------------------------------------------------------------------------------------------------------------------
#                                                                                                           Unit Testing
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    error_count = 0

    l.verbosity_override_set( True ) # we want to see ALL the logs for this unit test

    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )
    l.log( l.INFO,   "OGC.Engineering - Python3 Textual User Interface library unit test ( STARTING )" )
    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )

    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )
    l.log( l.INFO,   "OGC.Engineering - Python3 Textual User Interface library unit test ( ENDING )" )
    if ( error_count > 0 ):
        l.log( l.ERROR, "FAILED with error_count (%u)" % ( error_count ) )
    else:
        l.log( l.INFO, "PASSED" )
    l.log( l.NOTICE, "--------------------------------------------------------------------------------" )
