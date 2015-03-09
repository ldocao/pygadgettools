# pygadgettools
Python toolbox for basic analysis of GADGET data. 

Author : Long Do Cao

Date of creation : 27th January 2015






##last comments: test on new branch redesign


### REQUIREMENTS
* numpy
* pygadgetreader from R. Thompson


### pygadgettools
Package providing basic analysis for gadget data


### scripts
This directory contains some simple script to generate some 2D plots using YT, adapted to Gadget-2.


### initial_conditions
This directory contains some files to generate an initial condition file for Gadget-2 in binary format (format type=1 as defined in Gadget-2 user's guide). To use it, you need to have all the files in your working directory and follow the instructions below:

* insert "from write import *" at the beginning of your script
* create a header. For example : my_header=Header()
* create a body. For example : my_body=Body(npart) where npart is a 1D array containing the number of particles for each type
* Fill in the information in my_header and my_body with the same dimensions as defined in the _init_ method of each class. Be careful ! There is no security check at this point. If you replace for example an array by a single float number, the code currently authorizes this operation, but the Gadget-2 code will crash. You should follow the dimensions according to the Gadget-2 users guide. Currently, there is no sanity check but this should be improved in a next version. All array must be numpy array
* Once my_header and my_body are ready, you can write the initial condition file by calling the function dump_ic(my_header,my_body,my_name) where my_name is a string of the name of your ic_file.
* You can find an example in example.py