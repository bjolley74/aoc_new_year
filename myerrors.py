"""my error classes"""

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