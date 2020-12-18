"""
    AOC New Year
    -----------
    This is a python program to setup a new year for advent of code. It is a command line interface
    that will take an optional year and an optional file path to create the yearly advent of code project
    for the year given.
    
    The default year will be the current year when the program is run.
    
    The default path with be the directory that the program is run.
    
    Usage:
    python aoc_new_year.py <-v or --version -h or --help y:year d:file_path>
    
    Project Set Up
    -------------
    aoc_new_year.py will set up the following directory structure in <file_path>:
        [file_path]:
            [01]
                [data]
            [02]
                [data]
            [03]

            ...
            
            [25]
                [data]
    
"""


# import libraires
import os
import sys
import logging
from datetime import datetime
from glob import glob

now = datetime.now()
application_version = '2020-12-1.0'

#get system arguments
args = sys.argv

#    logger set up
name, ext = args.pop(0).split('.')
log_file = f'{name}.log' 
log_level = logging.DEBUG
f = '%(asctime)-15s: %(levelname)-8s: %(message)s'
logging.basicConfig(level=log_level, filename=log_file, filemode='a+', format=f)
logger = logging.getLogger(__name__)
logger.info(f'\n\n\n\t\t******{name}.{ext}: {now} ******\n')

class ArgumentError(Exception):
    """
    ArgumentError is raised when aoc_new_year.py is given an unexpected argument. Expected arguments
    include '-h', '--help', '-v', '--version', 'y:1234',and/or 'd:filepath/'. Any other arguments
    provided will result in an ArgumentError
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f'"{self.message}"'
    
    def __repr__(self):
        return "<class 'ArgumentError'>"

class YearY2KError(Exception):
    """
    What? You Want Y2K all over again? A YearY2KError is raised if aoc_new_year.py is given a 
    year via the command line that is less than a 4 digit year.
    
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f'"{self.message}"'
    def __repr__(self):
        return "<class 'YearY2Error'>"

def log_wrap(pre, post):
    """Wrapper"""
    def decorate(func):
        """Decorater"""
        def call(*args,**kwargs):
            """Actual Wrapper"""
            pre(func)
            result = func(*args, **kwargs)
            post(func)
            return result
        return call
    return decorate


def entering(func):
    """Pre function logging"""
    logger.debug(f"entered {func.__name__}")


def exiting(func):
    """Post function logging"""
    logger.debug(f"exiting {func.__name__}")

@log_wrap(entering, exiting)
def print_help():
    """Prints out the help menu"""
    help_menu = """
    AdventOfCode HELP MENU
    ----------------------
    
    python aoc_new_year.py <-v or --version -h or --help y:year d:file_path>
    
    options:
    -------
    -v or --version             display application version
    -h or --help                display help menu
    y:<year>                   set 4 digit year that application will use
    d:<file path>              set file path that application will place project in

    """
    print(help_menu)
    my_exit()


def my_exit(msg=''):
    """Prints out any msg provided and performs sys.exit()"""
    print(msg)
    sys.exit()


@log_wrap(entering, exiting)
def main(year, path):
    """
    Main logic of the program
    """
    directories_made = ['\n']
    # change directory to path
    try:
        os.chdir(path)
        logger.debug(f'stepped into {os.getcwd()} directory')
    except OSError as err:
        logger.critical(f"Error occured while attempting to change directory to {path}")
        raise err
    # make directory with year
    try:
        os.mkdir(str(year))
        directories_made.append(f'{str(year)}/')
        logger.debug(f'mkdir {year} directory in {os.getcwd()} directory')
    except OSError as err:
        msg = f'An unexpected error occured while making {year} directory'
        logger.critical(f"{msg}: {err}")
        raise OSError(msg)
    # change directory to year directory
    try:
        os.chdir(str(year))
        logger.debug(f'stepped into {year} directory')
    except OSError as err:
        msg = f'An unexpected error occured while entering {year} directory'
        logger.critical(f"{msg}: {err}")
        raise OSError(msg)
    # loop through numbers 0-9
    for x in range(10):
        num_str = '0' + str(x)
        # make directory with number  string
        os.mkdir(num_str)
        directories_made.append(f'  {year}/{num_str}/')
        logger.debug(f'made {num_str} directory')
        # make data directory in 0x directory
        os.mkdir(num_str + '/data')
        directories_made.append(f'    {year}/{num_str}/data/')
        logger.debug(f'made {num_str}/data directory')
    # loop through numbers 10 - 25
    for x in range(10,26):
        # make directory with number string
        os.mkdir(str(x))
        directories_made.append(f'  {year}/{x}/')
        logger.debug(f'made {x} directory')
        # make data directory in x directory
        os.mkdir(str(x) + '/data')
        directories_made.append(f'    {year}/{x}/data')
        logger.debug('made {x} directory')
    print(f'\nDirectory structure in {os.getcwd()}:')
    for directory in directories_made:
        print(directory)


if __name__ == "__main__":
    # process arguments
    arg_keywords = {}
    if len(args) >= 1:
        if '-h' in args or '--help' in args:
            print_help()
        elif '-v' in args or '--version' in args:
            print(f"\tAdventOfCode New Year\n\taoc_new_year.py\n\tVersion {application_version}")
            my_exit()
        else:
            args = [x.split(' ') for x in args]
            for arg in args:
                if str(type(arg)) == "<class 'list'>":
                    for a in arg:
                        if 'y:' in a or 'd:' in a:
                            key, value = a.split(':')
                            arg_keywords[key.lower()] = value
                        else:
                            message = f'Invalid argument received: {args}'
                            logger.critical(message)
                            raise ArgumentError(message)
                else:
                    if 'y:' in arg or 'd:' in arg:
                        key, value = arg.split(':')
                        arg_keywords[key.lower()] = value
                    else:
                        message = f'Invalid argument received: {args}'
                        logger.critical(message)
                        raise ArgumentError(message)
    try:
        # setting year to argument received or to current year
        year = int(arg_keywords.get('y', now.year))
    except ValueError as err:
        # if year provided is not a number log and raise error
        logger.critical(f'ValueError \'{err}\' occured while setting up year: value entered is not a number - {arg_keywords.get("y")}')
        raise err
    # make sure that year is a 4 digit year if not will log and raise error
    if len(str(year)) < 4:
        msg = f"Year provided is not 4 digit year: '{year}'"
        logger.critical(f'YearY2KError: {msg}')
        raise YearY2KError(msg)
    # setting path to argument provided or to current directory
    path = arg_keywords.get('d', '.')
    # check if path exists, if not log and raise an OSError
    if not os.path.exists(path):
        message = f"Path '{path}' does not exist"
        logger.critical(f'OSError: {message}')
        raise OSError(message)
    main(year, path)
    my_exit(msg='\n\nProgram complete with no errors, Goodbye!')