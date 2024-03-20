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
* provide customized logging library that allows multiple targets for a log file
    * customized formatting - this is how I like to see my logs
    * thresholding with simple override
    * default logging to console
    * optional logging to file
    * optional logging to a queue for application handling
