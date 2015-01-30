###NAME: filename.py
###PURPOSE: filename handling



import os,sys,warnings


def getFullPath(n,root="snapshot_",dir="./",ndigits=3,ext=""):
    """
    PURPOSE: return the absolute path of file to read
    INPUTS : n = number of snapshot
             root = name of snapshot
             dir = directory of files
             ext = extension to file
             ndigits = number of digits to add leading zeros
    COMMENTS : 1. currently assume one single file to read for a given time.
    """

    numbering=str(n).zfill(ndigits) ##add leading zeros
    dir=os.path.join(dir, '') #append '/' character if needed
    input_file=dir+root+numbering+ext

    return input_file

