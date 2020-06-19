# Airfoil_Analysis
This python code is developed by Sreemannarayana Ikkurthi,
as a part of course notes for the course 15AES302: Aerodynamics II, in the year 2019-20

In support of Dr. Rajesh Senthil Kumar T.,
Assistant Professor, 

Department of Aerospace Engneering, Amrita Vishwa Vidyapeetham.

Analyse any airfoil from UIUC database in xfoil and obtain cp and polar values

The zip file consists of Database folder, Results folder, Xfoil folder, Airfoil Analysis.ipynb

Database folder consists of all the airfoils in UIUC airfoil data files in .dat or .DAT format.

Results folder consists of all the output files from xfoil.

Xfoil folder consists of xfoil program.

Airfoil Analysis.ipynb is the python 3 Jupyter notebook file, where the source code is available for modification and execution.

## Source code info

The code consists of a class and several functions for analysing an airfoil in xfoil program.

The code by default selects a random airfoil from the UIUC database and apply spline to upper and lower surface of airfoil and produce required number of points for analysis.
These new coordinates are analysed in xfoil with the given input variables.

The INPUTS section contains pts, Re, Mach, N_crit, Alpha variables

           pts = No. of points for spline

           Re =  Reynolds number

           Mach = Mach number

           N_crit =  Critical boundary layer interaction

           Alpha = Angle of attack

If any specific airfoil is to be analysed then it can be entered to foil variable in THE CODE section.
