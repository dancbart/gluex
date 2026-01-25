The Makefile in this directory was created to compile 'flatten.cc' on the Old Dominion Wahab server, namely wahab.hpc.odu.edu.

The reason it was necessary is the ODU server didn't have a shared copy of ROOT (or I couldn't find it).  So I created a virtual environment with conda, installed python inside, and importantly a version of CERN's ROOT software.

However, upon compile of 'flatten' for FSRoot, located in the Github repo hd_utilities, here https://github.com/JeffersonLab/hd_utilities/tree/master/FlattenForFSRoot the g++ compiler looked in the system "include" folder and there was a mis-match of header files.  

SOLUTION:
The Makefile in this directory explicitly unsets the default system "include" directory, then explicitly sets all the necessary "include" directories residing in the version of ROOT installed by Conda.

This may break upon future re-compiles. But the takeaway from the exercise was to lock the compile process down to ONLY look inside the directories in the virtual environment created by Conda, and it's encapsulated ROOT install.  i.e. to force it NOT to look at the ODU server's default "include" directories.
