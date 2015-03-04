import numpy as np
import os
import sys




class Header:
    """Structure of the header for initial condition file

    Parameters
    ----------

    None

    Comments
    --------

    Please note that NumPart_Total_HW, nor Flag_Entropy_ICs are defined in header. Need to be implemented
    
    """
    
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

        
    """

    def __init__(self, npart,
           rho, ne, nh, hsml,
           acce, endt, tstp):

        total_number_of_particles = np.sum(npart,dtype="float64")
        gas_particles=npart[0] #number of gas particles

        self.pos = np.zeros([total_number_of_particles,3]) #Positions
        self.vel = np.zeros([total_number_of_particles,3]) #Velocities
        self.id  = np.zeros(total_number_of_particles)     #Particle ID's
        self.mass =  np.zeros(total_number_of_particles)   #Masses
        self.u =  np.zeros(gas_particles)                  #Internal energy per unit mass

        ##initialize only if enable in makefile to save memory. Maybe there is a smarter way to do that. But the idea is that if you need for example acce, you need all the blocks before.
        if tstp:
            rho = True
            ne = True
            nh = True
            hsml = True
            pot = True
            acce = True
            endt = True
            self.tstp =np.zeros(total_number_of_particles)

        if endt:
            rho = True
            ne = True
            nh = True
            hsml = True
            pot = True
            acce = True
            self.endt =np.zeros(gas_particles)

        if acce:
            rho = True
            ne = True
            nh = True
            hsml = True
            pot = True
            self.acce =np.zeros(total_number_of_particles)

        if pot:
            rho = True
            ne = True
            nh = True
            hsml = True
            self.pot = np.zeros(total_number_of_particles)            

        if hsml:
            rho = True
            ne = True
            nh = True
            self.hsml =np.zeros(gas_particles) #SPH Smoothing Length

        if nh:
            rho = True
            ne = True
            self.nh = np.zeros(gas_particles) #Hydrogen Abundance

        if ne:
            rho = True
            self.ne = np.zeros(gas_particles) #Electron Abundance

        if rho:
            self.rho =np.zeros(gas_particles) #Density





# def check_if_file_exists(filename):
#     """Check if the file exists in the current directory

#     """
#     check=True

#     return check




# def check_header(header):
#     """Run a series of tests to check the header

#     """
#     return None

# def check_body(body):
#     """Run a series of tests to check the body
    
#     """
#     return None





def write_header(header, icfile,format=1):
    """Write the header into a specified already open file

    Parameters
    ----------

    header : object
       see Class structure defined in this file

    icfile : ??
       file identifier when opening file in python

    format : integer
       format of desired initial condition (1:binary, 3:hdf5). Only binary 1 is implemented

    Comments
    --------

    Please note that NumPart_Total_HW, nor Flag_Entropy_ICs will be written to the header. Need to be implemented
    """

    
    #* Note that we use struct.pack to form a block, whereas we have to use tostring() on a non-block *#
    #write header into file
    print "Writing header (little endian)..."
    icfile.write(struct.pack('<I',256))                             #dummy
    icfile.write(struct.pack('<6I',
                             header.NumPart_ThisFile[0],
                             header.NumPart_ThisFile[1],
                             header.NumPart_ThisFile[2],
                             header.NumPart_ThisFile[3],
                             header.NumPart_ThisFile[4],
                             header.NumPart_ThisFile[5]))
    icfile.write(struct.pack('<6d',
                             header.MassTable[0],
                             header.MassTable[1],
                             header.MassTable[2],
                             header.MassTable[3],
                             header.MassTable[4],
                             header.MassTable[5]))
    icfile.write(struct.pack('<d',header.Time))                            #a
    icfile.write(struct.pack('<d',header.Redshift))                        #z
    icfile.write(struct.pack('<i',header.Flag_Sfr))                         #sfrFlag
    icfile.write(struct.pack('<i',header.Flag_Feedback))                          #FBFlag
    icfile.write(struct.pack('<6I',
                             header.NumPart_Total[0],
                             header.NumPart_Total[1],
                             header.NumPart_Total[2],
                             header.NumPart_Total[3],
                             header.NumPart_Total[4],
                             header.NumPart_Total[5]))
    icfile.write(struct.pack('<i',header.Flag_Cooling))                     #coolingFlag    
    icfile.write(struct.pack('<i',header.NumFilesPerSnapshot))                               #numfiles
    icfile.write(struct.pack('<d',header.BoxSize))                              #boxsize
    icfile.write(struct.pack('<d',header.Omega0))                              #Omega_0
    icfile.write(struct.pack('<d',header.OmegaLambda))                              #Omega_Lambda
    icfile.write(struct.pack('<d',header.HubbleParam))                               #HubbleParam
    icfile.write(struct.pack('<i',header.Flag_StellarAge))
    icfile.write(struct.pack('<i',header.Flag_Metals))
    ##should add here NumPart_Total_HW. not implemented yet, nor Flag Entropy


    ##fill in empty space
    header_bytes_left = 260 - icfile.tell()
    for j in range(header_bytes_left):
        icfile.write(struct.pack('<x'))
    icfile.write(struct.pack('<I',256))
    if icfile.tell()-8 != 256:
        print('ERROR!  output header = %d' % icfile.tell()-8)
        sys.exit()

    return None






# def write_body(body, icfile):
#     """Write the body of initial condition file in a already open specified file


#     """
#     #### WRITE DATA
#     print "Writing data (little endian)..."

#     #convert to correct variable type
#     POS    = POS.astype('f')
#     VEL    = VEL.astype('f')
#     PID    = PID.astype('I')
#     MASSES = MASSES.astype('f') #variable particle mass (not needed if massarr is defined)
#     U      = U.astype('f')
#     RHO    = RHO.astype('f')
#     HSML   = HSML.astype('f')

    
#     #write in binary format
#     icfile.write(struct.pack('<I',3*4*sumnpart)) #dimensions*number of particles
#     icfile.write(POS.tostring())
#     icfile.write(struct.pack('<I',3*4*sumnpart))

#     #write velocity
#     icfile.write(struct.pack('<I',3*4*sumnpart))
#     icfile.write(VEL.tostring())
#     icfile.write(struct.pack('<I',3*4*sumnpart))

#     #write particles ID
#     icfile.write(struct.pack('<I',4*sumnpart))
#     icfile.write(PID.tostring())
#     icfile.write(struct.pack('<I',4*sumnpart))

#     #write variables mass particles
#     icfile.write(struct.pack('<I',4*sumnpart))
#     icfile.write(MASSES.tostring())
#     icfile.write(struct.pack('<I',4*sumnpart))
    
#     #write energy
#     icfile.write(struct.pack('<I',4*npart_total[0]))
#     icfile.write(U.tostring())
#     icfile.write(struct.pack('<I',4*npart_total[0]))

#     #write density
#     icfile.write(struct.pack('<I',4*npart_total[0]))
#     icfile.write(RHO.tostring())
#     icfile.write(struct.pack('<I',4*npart_total[0]))

#     # #write smoothing length
#     # icfile.write(struct.pack('<I',4*npart_total[0]))
#     # icfile.write(HSML.tostring())
#     # icfile.write(struct.pack('<I',4*npart_total[0]))

#     return None




def print_summary(header,body):
    """Print a summary of the parameters
    
    Parameters
    ----------
    
    header : class
       see Header Class

    body : class
       see Body Class
    """

    return None

def dump_ic(header, body, destination_file="ic.dat", format=1):
    """Generates output initial condition file for Gadget


    Parameters
    ----------
    header : object
        header for snapshot
    body : object
        body of snapshot (POS,VEL,MASS, etc.)
    destination_file : string
        output file name
    format : integer
        define output format as defined in Gadget-2
    """


    ##create ic_file
    if not check_if_file_exists(destination_file):
        icfile=open(destination_file,'w')

    ##run some sanity checks
    check_header(header)
    check_body(body)

    ##write the data
    write_header(header,icfile)
    write_body(body,icfile)

    ##finally close file and return
    print_summary(header,body)
    icfile.close()        
    return None











    




    


# def read_header(filename):
#     """
#     PURPOSE : read header from initial condition file
#     INPUTS : filename = name of file to read
#     OUTPUTS : header = header structure defined in class header
#     """

#     f=open(filename,'rb')
#     block=f.read(4)         ; dummy=struct.unpack('I',block)
#     block=f.read(4*6)       ; header.npart=struct.unpack('6I',block)#read number of particles
#     block=f.read(6*8)       ; header.mass=struct.unpack('6d',block) #read mass
#     block=f.read(8)         ; header.time=struct.unpack('d',block)#read time
#     block=f.read(8)         ; header.redshift=struct.unpack('d',block)#read redshift
#     block=f.read(4)         ; header.flag_sfr=struct.unpack('i',block)       
#     block=f.read(4)         ; header.flag_feedback=struct.unpack('i',block)  
#     block=f.read(6*4)       ; header.npart_total=struct.unpack('6I',block)   
#     block=f.read(4)         ; header.flag_cooling=struct.unpack('i',block)   
#     block=f.read(4)         ; header.num_files=struct.unpack('i',block)      
#     block=f.read(8)         ; header.BoxSize=struct.unpack('d',block)        
#     block=f.read(8)         ; header.omega_zero=struct.unpack('d',block)     
#     block=f.read(8)         ; header.omega_lambda=struct.unpack('d',block)   
#     block=f.read(8)         ; header.hubbleparam=struct.unpack('d',block)    
#     block=f.read(4)         ; header.flag_stellarage=struct.unpack('i',block)
#     block=f.read(4)         ; header.flag_metals=struct.unpack('i',block)    

#     f.close()

#     return header


