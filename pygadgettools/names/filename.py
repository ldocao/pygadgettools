###NAME: filename.py
###PURPOSE: filename handling

import os



def get_full_path(n,root="snapshot_",dir="./",ndigits=3,ext=""):
    """Return the absolute path of file to read

    Parameters:
    ----------

    n : integer
        snapshot number

    root : string 
        root name of snapshot

    dir : string
        directory of files

    ext : string
        extension of file

    ndigits : integer
        number of digits to add leading zeros

    COMMENTS : 1. currently assume one single file to read for a given time.
    """

    numbering=str(n).zfill(ndigits) ##add leading zeros
    dir=os.path.join(dir, '') #append '/' character if needed
    input_file=dir+root+numbering+ext

    return input_file

