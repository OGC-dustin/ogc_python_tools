# OGC.Engineering
## ogc_python_tools - A collection of python tools and libraries
Developer contact - dustin ( at ) ogc.engineering

---
## Repository Information
* Purpose
    - Create reusable python tools to achieve common tasks for anyone to use
* Clone
    - Navigate to your project repository and add ogc-python-tools as a submodule
```
git submodule add https://github.com/OGC-dustin/ogc_python_tools.git
```
* Future clones of your repository
```
git clone <however_you_clone_your_repo>
git submodule update --init
```
* Run unit test by calling the library file directly
```
python3 <path/to/library_of_interest>.py
```
* Import into your python3 project 
```
import ogc_python_tools.ogc_python_logging as l
```

# Tools

## ogc_python_logging
* Customized logging library:
    * customized formatting - this is how I like to see my logs
    * thresholding with simple override
        - Level filtering starts at "FATAL" messages and adds levels from there
        - FATAL - Program failure, no resolution beyond restarting
            * Address these ASAP with a 3 a.m. call to engineering, all hands on deck, etc.
        - ERROR - Program fault, recoverable, but at reduced capacity
            * Address these on the next business day with a patch release if possible
        - WARNING - Warnings indicate edge cases and other areas where developers knew a problem could occur and provided a way to handle it
            * Address these in the next revision
        - NOTICE - Important enough that they need to be sent externally for support evaulation without prompting special action
            * Used to indicate status of remote updates, send responses to requests, etc. without alerting the need for special attention
        - INFO - Most common level logging level that give "information" about the system that is not important enough to be sent externally
            * When logged into or connected to a system, INFO logs should show a support user enough information to track device operations
        - DEBUG - Every major decision or fork in operation use in "debugging" operations
            * Enough information to trace a problem but not enough to overwhelm
        - TRACE - Every step inbetween use to "trace" a program through every detail of operation
            * Typically only used during develpoment or major debugging events
    * default logging to console
    * optional logging to file
    * optional logging to a queue for application handling
