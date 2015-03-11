###NAME: sanity_check.py
###PURPOSE: sanity check routines

def _check_if_keyword_is_correct(sys,list_authorized):
    """Check if the input sys are known
    """

    if sys not in list_authorized:
        raise KeyError, sys+" must be ["+", ".join(list_authorized)+"]"


def _check_dimension(x,dim):
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
