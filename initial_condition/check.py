import sys
import numpy as np

def check_if_file_exists(filename):
    """Check if the file exists in the current directory

    """

    return None


def check_header(Header):
    """Run a series of tests to check the header

    """
    print "Checking header..."
    ##check if there are some particles
    if (np.sum(Header.NumPart_ThisFile) == 0) or (np.sum(Header.NumPart_Total) == 0):
        print "No particles in header !"
        sys.exit()


    return None

def check_body(Body):
    """Run a series of tests to check the body
    
    """
    return None



def check_consistency(Header, Body):
    """Run a series of test to check consistency between body and header

    Parameters
    ----------
    
    Header : object
        see Class Header
        
    Body : object
        see Class Body
    """

    ##check dimensions

    return None



def print_summary(Header,Body):
    """Print a summary of the parameters
    
    Parameters
    ----------
    
    header : class
       see Header Class

    body : class
       see Body Class
    """
    from pprint import pprint


    ##print header attributes
    pprint (vars(Header))

    ##print body summary

    return None

