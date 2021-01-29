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

import os
import sys
import logging
from datetime import datetime
from glob import glob
import argparse
from myerrors import ArgumentError, YearY2KError

now = datetime.now()
prog_name = 'aoc_new_year'

#    logger set up
log_file = f'{prog_name}.log' 
log_level = logging.DEBUG
f = '%(asctime)-15s: %(levelname)-8s: %(message)s'
logging.basicConfig(level=log_level, filename=log_file, filemode='a+', format=f)
logger = logging.getLogger(__name__)
with open(log_file, 'a+') as log:
    log.write(f'************** {now} ********************')

#get system arguments
text = f"""{prog_name} will rename and move files into folder based 
on the year, month and date that the photo was taken"""
parser = argparse.ArgumentParser(prog=prog_name, description=text)
year = now.year
parser.add_argument('year', metavar='Y', default=year, type=str,
                   help='set 4 digit year that application will use to create directories')
parser.add_argument('path', metavar='D', default='./', type=str, 
                   help='set file path in which the application will place project')
parser.add_argument('-v, --version', action='version', version='%(prog)s 2021.01.1')

args = parser.parse_args()

logger.debug(f'arguments received: {args}')

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


def my_exit(msg=''):
    """Prints out any msg provided and performs sys.exit()"""
    print(msg)
    print('Goodbye!')
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
    created_dir = path + '\\' + str(year)
    return os.path.exists(created_dir)


if __name__ == "__main__":
    # process arguments
    try:
        year = int(args.year)
    except ValueError as err:
        # if year provided is not a number log and raise error
        logger.critical(f'ValueError \'{err}\' occured while setting up year: value entered is not a number - {args.year}')
        raise err
    # make sure that year is a 4 digit year if not will log and raise error
    if len(str(year)) < 4:
        msg = f"Year provided is not 4 digit year: '{year}'"
        logger.critical(f'YearY2KError: {msg}')
        raise YearY2KError(msg)
    # setting path to argument provided or to current directory
    path = args.path
    # check if path exists, if not log and raise an OSError
    if not os.path.exists(path):
        message = f"Path '{path}' does not exist"
        logger.critical(f'OSError: {message}')
        raise OSError(message)
    main_return = main(year, path)
    if main_return:
        logger.info('main returned True, directory successfully created')
        my_exit(msg='\n\nProgram complete...')
    else:
        logger.warning('main returned False, directory not created')
        my_exit(msg='\n\nProgram complete with errors. Please check log...')
