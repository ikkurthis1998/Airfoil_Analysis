# Airfoil_Analysis
Analyse any airfoil from UIUC database in xfoil and obtain cp and polar values

The zip file consists of Database folder, Results folder, Xfoil folder, Air Code.ipynb

Database folder consists of all the airfoils in UIUC airfoil data files in .dat or .DAT format
Results folder consists of all the output files from xfoil
Xfoil folder consists of xfoil program
Air Code.ipynb is the python 3 Jupyter notebook file, where the source code is available for modification and execution.

## Source code info

The code consists of a class and several functions for analysing an airfoil in xfoil program.

# xfoil class: 
The xfoil class consists of two major functions: 1. cp_oper 2. polar oper

cp_oper: 
           Inputs: file_name, Re, Mach, N_crit, Alpha
                  file_name: Name of the airfoil data file
                  Re       : Reynolds number of flow
                  N_crit   : Critical boundary layer interaction number
                  Alpha    : Angle of attack at which cp is needed
           Function: Obtain cp values at given angle of attack and save them to Results folder
           Output: returns cp as output
        
polar_oper: 
           Inputs: file_name, Re, Mach, N_crit, Alpha
                  file_name: Name of the airfoil data file
                  Re       : Reynolds number of flow
                  N_crit   : Critical boundary layer interaction number
                  Alpha    : Angle of attack at which cp is needed
           Function: Obtain cl, cd, cm values for given angle of attack and save them to Results folder
           Output: Array of angle of attack, cl, cd, cm

# Important functions:
seperate_airfoil:
            Inputs: x, y coordinates of airfoil
            Function: Seperate the upper and lower coordinates of airfoil
            Output: xu, yu, xl, yl
                    xu: upper x coordinates
                    yu: upper y coordinates
                    xl: lower x coordinates
                    yl: lower y coordinates
                  
xtra_pts:
