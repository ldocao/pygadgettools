import numpy as np
import os
import sys
import struct
from check import *





class Header:
    """Structure of the header for initial condition file

    Parameters
    ----------

    None

    Comments
    --------

    (1) Please note that NumPart_Total_HW, nor Flag_Entropy_ICs are defined in header. Need to be implemented
    (2) Naming conventions follows users-guide.pdf of Gadget-2 for attribute names
    
    """
    
    ##A possible improvement would be to freeze the attribute structure. Maybe we can start by looking at  http://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init


    ##naming use HDF5 identifier
    def __init__(self):
        self.NumPart_ThisFile    = np.zeros(6) #number of particles of each type in present file
        self.MassTable           = np.zeros(6) #mass of each particle type
        self.Time                = 0 #time of output, or expansion factor for cosmo simu
        self.Redshift            = 0 #redshift
        self.Flag_Sfr            = int(0) #flag star formation (unused in GADGET2)
        self.Flag_Feedback       = int(0) #flag feedback (unused in GADGET2)
        self.NumPart_Total       = np.zeros(6,dtype=np.int8) #total number of particles of each type in simulation
        self.Flag_Cooling        = int(0) #flag for cooling
        self.NumFilesPerSnapshot = int(1) #number of files in each snapshot
        self.BoxSize             = 0 #box size if periodic boundary condition
        self.Omega0              = 0 #matter density at z=0
        self.OmegaLambda         = 0 #vaccum energy at z=0
        self.HubbleParam         = 0 #hubble constant
        self.Flag_StellarAge     = int(0) #creation times of stars (unused)
        self.Flag_Metals         = int(0) #flag mettalicity (unused)

        ##not implemented yet
        # self.NumPart_Total_HW    = 0 #not implemented yet. assume number of particles  <2^32
        # self.Flag_Entropy_ICs    = 0




class Body:
    """Structure of body for initial condition file

    Parameters
    ----------
    
    npart : integer array (6)
        Number of particles for each type

    rho : boolean
        Density will be in initial condition file
        
    ne : boolean
        Electron abundance will be in initial condition file

    nh : boolean
        Hydrogen abundance will be in initial condition file

    hsml : boolean
        SPH smoothing length will be in initial condition file

    pot : boolean
        Gravitational potential enable in Makefile ?
        
    acce : boolean
        Acceleration of particles enable in Makefile ?

    endt : boolean
        Rate of change of entropic function of SPH particles enable in Makefile ?
   
    tstp : boolean
        Timestep of particles enable in Makefile ?

        
    Comments:
    --------

    (1) For the moment, all boolean optional keywords are useless.
    """

    def __init__(self, npart,
           rho=False, ne=False, nh=False, hsml=False,
           acce=False, endt=False, tstp=False):

        npart=np.array(npart) #make sure it is a numpy array
        total_number_of_particles = np.sum(npart,dtype="float64")
        gas_particles=npart[0] #number of gas particles

        if total_number_of_particles != 0. :
            self.pos = np.zeros([total_number_of_particles,3]) #Positions
            self.vel = np.zeros([total_number_of_particles,3]) #Velocities
            self.id  = np.zeros(total_number_of_particles)     #Particle ID's
            self.mass =  np.zeros(total_number_of_particles)   #Masses
        else:
            raise ValueError, "There are no particles !"

        self.u =  np.zeros(gas_particles)                  #Internal energy per unit mass





        # ##initialize only if enable in makefile to save memory. Maybe there is a smarter way to do that. But the idea is that if you need for example acce, you need all the blocks before. Need to be implemented
        # if tstp:
        #     rho = True
        #     ne = True
        #     nh = True
        #     hsml = True
        #     pot = True
        #     acce = True
        #     endt = True
        #     self.tstp =np.zeros(total_number_of_particles)

        # if endt:
        #     rho = True
        #     ne = True
        #     nh = True
        #     hsml = True
        #     pot = True
        #     acce = True
        #     self.endt =np.zeros(gas_particles)

        # if acce:
        #     rho = True
        #     ne = True
        #     nh = True
        #     hsml = True
        #     pot = True
        #     self.acce =np.zeros(total_number_of_particles)

        # if pot:
        #     rho = True
        #     ne = True
        #     nh = True
        #     hsml = True
        #     self.pot = np.zeros(total_number_of_particles)            

        # if hsml:
        #     rho = True
        #     ne = True
        #     nh = True
        #     self.hsml =np.zeros(gas_particles) #SPH Smoothing Length

        # if nh:
        #     rho = True
        #     ne = True
        #     self.nh = np.zeros(gas_particles) #Hydrogen Abundance

        # if ne:
        #     rho = True
        #     self.ne = np.zeros(gas_particles) #Electron Abundance

        # if rho:
        #     self.rho =np.zeros(gas_particles) #Density










def write_header(header, ic_file, format_output=1):
    """Write the header into a specified already open file

    Parameters
    ----------

    header : object
       see Class Header defined in this file

    ic_file : object
       file identifier when opening file in python

    format_output : integer
       format of desired initial condition (1:binary, 3:hdf5). Only binary 1 is implemented

    Comments
    --------

    Please note that NumPart_Total_HW, nor Flag_Entropy_ICs will be written to the header. Need to be implemented
    """

    print "Writing header (little endian)"
    #* Note that we use struct.pack to form a block, whereas we have to use tostring() on a non-block *#
    #write header into file
    ic_file.write(struct.pack('<I',256))                             #dummy
    ic_file.write(struct.pack('<6I',
                             header.NumPart_ThisFile[0],
                             header.NumPart_ThisFile[1],
                             header.NumPart_ThisFile[2],
                             header.NumPart_ThisFile[3],
                             header.NumPart_ThisFile[4],
                             header.NumPart_ThisFile[5]))
    ic_file.write(struct.pack('<6d',
                             header.MassTable[0],
                             header.MassTable[1],
                             header.MassTable[2],
                             header.MassTable[3],
                             header.MassTable[4],
                             header.MassTable[5]))
    ic_file.write(struct.pack('<d',header.Time))                            #a
    ic_file.write(struct.pack('<d',header.Redshift))                        #z
    ic_file.write(struct.pack('<i',header.Flag_Sfr))                         #sfrFlag
    ic_file.write(struct.pack('<i',header.Flag_Feedback))                          #FBFlag
    ic_file.write(struct.pack('<6I',
                             header.NumPart_Total[0],
                             header.NumPart_Total[1],
                             header.NumPart_Total[2],
                             header.NumPart_Total[3],
                             header.NumPart_Total[4],
                             header.NumPart_Total[5]))
    ic_file.write(struct.pack('<i',header.Flag_Cooling))                     #coolingFlag    
    ic_file.write(struct.pack('<i',header.NumFilesPerSnapshot))                               #numfiles
    ic_file.write(struct.pack('<d',header.BoxSize))                              #boxsize
    ic_file.write(struct.pack('<d',header.Omega0))                              #Omega_0
    ic_file.write(struct.pack('<d',header.OmegaLambda))                              #Omega_Lambda
    ic_file.write(struct.pack('<d',header.HubbleParam))                               #HubbleParam
    ic_file.write(struct.pack('<i',header.Flag_StellarAge))
    ic_file.write(struct.pack('<i',header.Flag_Metals))
    ##should add here NumPart_Total_HW. not implemented yet, nor Flag Entropy


    ##fill in empty space
    header_bytes_left = 260 - ic_file.tell()
    for j in range(header_bytes_left):
        ic_file.write(struct.pack('<x'))
    ic_file.write(struct.pack('<I',256))
    if ic_file.tell()-8 != 256:
        raise IOError, "header has wrong format"


    return None






def write_body(body, ic_file, format_output):
    """Write the body of initial condition file in a already open specified file

    Parameters
    ----------

    body : object
       see Class Body defined in this file

    ic_file : object
       file identifier when opening file in python

    format_output : integer
       format of desired initial condition (1:binary, 3:hdf5). Only binary 1 is implemented

    """

    print "Writing body (little endian)"

    def write_block(block, nbytes, ic_file):
        """Write a block from the body structure

        Parameters
        ----------
        
        block : float array
           The data block to be written.

        nbytes : float
           Size of the block

        ic_file ; Object
           File identifier to write in
            
        """

        ic_file.write(struct.pack('<I',nbytes)) #dimensions*number of particles
        ic_file.write(block.tostring())
        ic_file.write(struct.pack('<I',nbytes))

        return None

    total_number_of_particles = np.size(body.pos[:,0])
    gas_particles = np.size(body.u)

    
    #write in binary format
    write_block(body.pos.astype('f'), 3*4*total_number_of_particles, ic_file)
    write_block(body.vel.astype('f'), 3*4*total_number_of_particles, ic_file)
    write_block(body.id.astype('I'), 4*total_number_of_particles, ic_file)
    write_block(body.mass.astype('f'), 4*total_number_of_particles, ic_file)
    write_block(body.u.astype('f'), 4*gas_particles, ic_file)


    # ##need to set conditions to write these blocks. Maybe it's better to do a loop over each block, but it need some more work.
    # write_block(body.rho.astype('f'), 4*gas_particles, ic_file)
    # write_block(body.ne.astype('f'), 4*gas_particles, ic_file)
    # write_block(body.nh.astype('f'), 4*gas_particles, ic_file)
    # write_block(body.hsml.astype('f'), 4*gas_particles, ic_file)
    
    return None













def dump_ic(header, body, destination_file="ic.dat", format_output=1):
    """Generates output initial condition file for Gadget


    Parameters
    ----------
    header : object
        header for snapshot.
    body : object
        body of snapshot (POS,VEL,MASS, etc.)
    destination_file : string
        Full path of the output file name.
    format_output : integer
        Define output format as defined in Gadget-2. Only Binary 1 supported for now.

      
    """


    ##create ic_file
    if not check_if_file_exists(destination_file):
        ic_file=open(destination_file,'w')

    ##run some sanity checks.
    check_header(header)
    check_body(body)
    check_consistency(header,body)

    ##write the data
    write_header(header,ic_file,format_output)
    write_body(body,ic_file,format_output)

    ##finally close file and return
    print "=== SUMMARY ==="
    print_summary(header,body)
    ic_file.close()        
    return None









