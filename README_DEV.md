#pygadgettools


This is the README for developers.


It is redundant to either import only what is necessay in the main __init__.py or specify the __all__ variable at the beginning of each modules and then do a from module import *

I decide to import * in the main __init__.py and add the __all__ variable in each module to define what is available directly to the user, and what is not. 

While it's not mandatory to put a leading underscore before private methods, it is recommended to add a leading underscore for private and two leading underscore for superprivate methods or variables.