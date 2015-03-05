import sys
import numpy as np



def check_dimension(x,dim):
    """Check if x has dimension dim
    
    Parameters
    ----------
    
    x : array
       array to be tested
    dim : array
       required dimensions
    
    """

    if np.shape(x) != dim:
        raise Exception, "Unexpected dimensions"
    
    return None




def check_if_file_exists(filename):
    """Check if the file exists in the current directory

    """

    return None


def check_header(header):
    """Run a series of tests to check the header

    """
    print "Checking header..."

    ##check if there are some particles
    if (np.sum(header.NumPart_ThisFile) == 0) or (np.sum(header.NumPart_Total) == 0):
        raise ValueError,"No particles in header !"

    ##check if mass are positive
    if np.any(header.MassTable < 0):
        raise ValueError, "MassTable contains negative values"

    ##check if NumFilesPerSnapshot is positive
    if header.NumFilesPerSnapshot <= 0:
        raise ValueError, "NumFilesPerSnapshot is less or equal 0"

    ##check if number of particles have good dimensions
    check_dimension(header.NumPart_ThisFile, (6,))
    check_dimension(header.NumPart_Total, (6,))
    check_dimension(header.MassTable, (6,))
    

    return None



def check_body(body):
    """Run a series of tests to check the body
    

    Parameters
    ----------

    body : Object
       see Class Object
    """
    
    return None



def check_consistency(header, body):
    """Run a series of test to check consistency between body and header

    Parameters
    ----------
    
    header : object
        see Class Header
        
    body : object
        see Class Body
    """


    ##check dimensions
    npart=header.NumPart_ThisFile #assume there is only one file
    gas_particles=npart[0]
    total_number_of_particles=np.sum(npart,dtype="float64")

    check_dimension(body.pos, (total_number_of_particles,3))
    check_dimension(body.vel, (total_number_of_particles,3))
    check_dimension(body.mass, (total_number_of_particles))
    check_dimension(body.id, (total_number_of_particles,))
    
    if gas_particles != 0:
        check_dimension(body.u, (gas_particles,))
    

    ##check unicity of ID
    if np.size(np.unique(body.id)) !=  np.size(body.id):
        raise Exception, "IDs are not unique"


    return None



def print_summary(header,body):
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
    pprint (vars(header))

    ##print body summary

    return None

