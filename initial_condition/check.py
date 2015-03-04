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
        raise ValueError,"No particles in header !"

    ##check if mass are positive
    if np.any(Header.MassTable < 0):
        raise ValueError, "MassTable contains negative values"

    ##check if NumFilesPerSnapshot is positive
    if Header.NumFilesPerSnapshot <= 0:
        raise ValueError, "NumFilesPerSnapshot is less or equal 0"

    ##check if number of particles have good dimensions
    if (np.shape(Header.NumPart_ThisFile) != (6,)) or (np.shape(Header.NumPart_Total) != (6,)) or (np.shape(Header.MassTable) != (6,)):
        raise Exception, "Particle numbers or MassTable has incorrect dimensions"


    return None

def check_body(Body):
    """Run a series of tests to check the body
    

    Parameters
    ----------

    Body : Object
       see Class Object
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
            raise Exception, "Incompatible dimensions with header"

        return None

    ##check dimensions
    npart=Header.NumPart_ThisFile #assume there is only one file
    gas_particles=npart[0]
    total_number_of_particles=np.sum(npart,dtype="float64")

    check_dimension(Body.pos, (total_number_of_particles,3))
    check_dimension(Body.vel, (total_number_of_particles,3))
    check_dimension(Body.mass, (total_number_of_particles))
    check_dimension(Body.id, (total_number_of_particles,))
    
    if gas_particles != 0:
        check_dimension(Body.u, (gas_particles,))
    

    ##check unicity of ID
    if np.size(np.unique(Body.id)) !=  np.size(Body.id):
        raise Exception, "IDs are not unique"


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

