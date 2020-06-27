
#################################### All the libraries imported are below #################################################
import subprocess as sp
import random
import os
import math
import numpy
import matplotlib.pyplot as plt
from scipy import interpolate
import shutil

###########################################################################################################################

################################################### INPUTS ################################################################
# Change the path according to your system
code_path = os.getcwd() + r'\\'
xfoil_path = code_path + r'\\Super_xfoil\Xfoil\\'
results_path = code_path + r'Results\\'

###################################### Defined functions below this #######################################################
class xfoil():

    def open_xfoil(self):
        ps = sp.Popen(xfoil_path + r'xfoil.exe', stdin=sp.PIPE)
        self.ps = ps

    def write_xfoil(self, inp):
        inp = bytes(inp, 'utf-8')
        self.ps.stdin.write(inp + b'\n')

    def close_xfoil(self):
        self.ps.stdin.close()
        self.ps.wait()

    # To get airfoil coordinates from xfoil. This can generate NACA 4 or 5 digit series airfoils.
    # air_code is the input variable which is NACA 4 or 5 digit code.
    # Saves the coordinates as .txt file.
    def get_airfoil(self, air_code):
        self.open_xfoil()
        self.write_xfoil(f'NACA {air_code}')
        self.write_xfoil('SAVE')
        self.write_xfoil(f'NACA {air_code} .txt')
        self.close_xfoil()
        (x, y) = extract.coordinates(f'NACA {air_code} .txt')
        return x, y

    def load_foil(self, file_name):
        self.open_xfoil()
        self.write_xfoil(f'LOAD')
        self.write_xfoil(f'{file_name}.dat')
        self.write_xfoil(f'{file_name}')

    def ini_oper(self, file_name, Re, Mach, N_crit):
        self.load_foil(file_name)
        self.write_xfoil(f'PCOP')
        self.write_xfoil(f'OPER')
        self.write_xfoil(f'Re')
        self.write_xfoil(f'{Re}')
        self.write_xfoil(f'Mach')
        self.write_xfoil(f'{Mach}')
        self.write_xfoil(f'VPAR')
        self.write_xfoil(f'N')
        self.write_xfoil(f'{N_crit}')
        self.write_xfoil(f'')

    # Saves the output of cp after operating on airfoil with given input
    def cp_oper(self, file_name, Re, Mach, N_crit, Alpha):
        self.ini_oper(file_name, Re, Mach, N_crit)
        self.write_xfoil(f'ALFA')
        self.write_xfoil(f'{Alpha}')
        self.write_xfoil(f'CPWR')
        self.write_xfoil(f'Cp_{file_name}_({Alpha}).txt')
        self.close_xfoil()
        copy_item(code_path, results_path, r'Cp_' + file_name + r'_(' + str(Alpha) + r')' + r'.txt')
        cp = extract.Cp(r'Cp_' + file_name + r'_(' + str(Alpha) + r')' + r'.txt')
        os.remove(r'Cp_' + file_name + r'_(' + str(Alpha) + r')' + r'.txt')
        return cp

    # Saves the output of polars after operating on airfoil with given input
    def polar_oper(self, file_name, Re, Mach, N_crit, Alpha):
        self.ini_oper(file_name, Re, Mach, N_crit)
        self.write_xfoil(f'PACC')
        self.write_xfoil(f'Polar_{file_name}.txt')
        self.write_xfoil(f'')
        self.write_xfoil(f'ALFA')
        self.write_xfoil(f'{Alpha}')
        self.close_xfoil()
        copy_item(code_path, results_path, r'Polar_' + file_name + r'.txt')
        (alpha, cl, cd, cdp, cm) = extract.polar(r'Polar_' + file_name + r'.txt')
        os.remove(r'Polar_' + file_name + r'.txt')
        return alpha, cl, cd, cdp, cm


# Removes unnecessary strings in a file
def remove_str(name):
    f = open(name, 'r+', errors='ignore')
    s = f.readlines()
    stror = len(s)
    n = len(s)
    count = 0
    i = 0
    while (count < n):
        coun = 0
        for j in range(len(s[i])):
            if (ord(s[i][j]) > 58):
                s.remove(s[i])
                coun = 1
            if coun == 1:
                break
        a1 = len(s)
        if (stror == a1):
            i = i + 1
        stror = a1
        count = count + 1
    f.truncate(0)
    f.seek(0)
    f.writelines(s)
    f.close()

class extract():
    # Extracts the airfoil coordinates from .dat file
    def coordinates(self, foil):
        remove_str(foil)
        with open(foil, 'r+', errors='ignore') as infile:
            dummy_x, dummy_y = numpy.loadtxt(infile, unpack=True, skiprows=0)
            x = dummy_x.tolist()
            y = dummy_y.tolist()
        if x[0] > 1:
            x = x[1:]
            y = y[1:]
        return x, y


    # Extracts the cp from the output file
    def Cp(self, foil):
        remove_str(foil)
        with open(foil, 'r+', errors='ignore') as infile:
            dummy = numpy.genfromtxt(infile, delimiter=[10, 9, 9], dtype=None).tolist()
            cp = [x[2] for x in dummy]
        return cp


    def polar(self, foil):
        remove_str(foil)
        with open(foil, 'r+', errors='ignore') as infile:
            dummy = numpy.genfromtxt(infile, delimiter=[9, 9, 9, 10, 9], dtype=float).tolist()
            alpha = [x[0] for x in dummy]
            cl = [x[1] for x in dummy]
            cd = [x[2] for x in dummy]
            cdp = [x[3] for x in dummy]
            cm = [x[4] for x in dummy]
        alpha = alpha[6:]
        cl = cl[6:]
        cd = cd[6:]
        cdp = cdp[6:]
        cm = cm[6:]
        return alpha, cl, cd, cdp, cm


# Create any number of random digit numbers.
# Input varaiables are n_digits and n_airfoils, n_digits is the number of digits of airfoil code.
# n_airfoils is the number of airfoil codes to be generated.
# It returns a list of airfoil codes.
def rand_digit(n_digits, n_airfoils):
    air_code = []
    for j in range(n_airfoils):
        code = ''
        for i in range(n_digits):
            code += str(random.randint(0, 9))
        air_code.append(code)
    return air_code


# seperate top and bottom half of airfoil.
# x is the x-coordinates of airfoil and y is the y-coordinates of airfoil.
# Returns xu, yu, xl, yl.
# xu is upper x-coordinates, yu is upper y-coordinates, xl is lower x-coordinates, yl is lower y-coordinates
def seperate_airfoil(x, y):
    count = 0
    for i in range(len(x) - 1):
        if x[count + 1] > x[count]:
            count += 1
        else:
            count = 0

    if (count + 1) < len(x):
        if x[0] > x[1]:
            xu = [x[0]]
            yu = [y[0]]
            xl = []
            yl = []
            for i in range(len(x) - 1):
                if x[i + 1] < x[i]:
                    xu.append(x[i + 1])
                    yu.append(y[i + 1])
                else:
                    break
            while i < (len(x) - 1):
                xl.append(x[i + 1])
                yl.append(y[i + 1])
                i += 1
            yl = [yl for xl, yl in sorted(zip(xl, yl))]
            xl = sorted(xl)
            if (xu[-1] != xl[0]) and (xl[0] != xl[1]):
                xl.insert(0, xu[-1])
                yl.insert(0, yu[-1])
            if xl[0] == xl[1]:
                xl.remove(xl[0])
                yl.remove(yl[0])
            return xu, yu, xl, yl
        else:
            xu = [x[0]]
            yu = [y[0]]
            xl = []
            yl = []
            for i in range(len(x) - 1):
                if x[i + 1] > x[i]:
                    xu.append(x[i + 1])
                    yu.append(y[i + 1])
                else:
                    break
            while i < (len(x) - 1):
                xl.append(x[i + 1])
                yl.append(y[i + 1])
                i += 1
            yl = [yl for xl, yl in sorted(zip(xl, yl))]
            xl = sorted(xl)
            if (xu[0] != xl[0]) and (xl[0] != xl[1]):
                xl.insert(0, xu[0])
                yl.insert(0, yu[0])
            if xl[0] == xl[1]:
                xl.remove(xl[0])
                yl.remove(yl[0])
            if xu[0] < xu[1]:
                xu = list(reversed(xu))
                yu = list(reversed(yu))
            return xu, yu, xl, yl
    else:
        xu = list(reversed(x))
        yu = list(reversed(y))
        xl = x[:]
        yl = y[:]
        return xu, yu, xl, yl


# Obtain extra points by interrpolating spline for given airfoil data from xu, yu, xl, yl.
# Inputs are xu, yu, xl, yl and pts. pts is the number of points required on each half of airfoil (upper and lower).
# Returns new coordinates. new_xu, new_yu, new_xl, new_yl.
def xtra_pts(x, y, pts):
    (xu, yu, xl, yl) = seperate_airfoil(x, y)

    yu_sorted = [yu for xu, yu in sorted(zip(xu, yu))]

    yl_sorted = [yl for xl, yl in sorted(zip(xl, yl))]

    sp_u = interpolate.PchipInterpolator(sorted(xu), yu_sorted, extrapolate=False)
    sp_l = interpolate.PchipInterpolator(sorted(xl), yl_sorted, extrapolate=False)

    theta_u = numpy.linspace(math.pi, 2 * math.pi, num=pts, endpoint=True)
    theta_u = theta_u.tolist()
    theta_l = numpy.linspace(0, math.pi, num=pts, endpoint=True)
    theta_l = theta_l.tolist()

    new_xu = []
    new_xl = []
    for i in range(len(theta_u)):
        new_xu.append(xu[-1] + (1 - (math.cos(theta_u[i]))) * ((abs(xu[-1] - xu[0])) / 2))
    for i in range(len(theta_l)):
        new_xl.append(xl[0] + (1 - (math.cos(theta_l[i]))) * ((abs(xl[-1] - xl[0])) / 2))

    new_yu = sp_u(new_xu)
    new_yu = new_yu.tolist()

    new_yl = sp_l(new_xl)
    new_yl = new_yl.tolist()

    if new_xu[-1] == new_xl[0]:
        new_xl = new_xl[1:]
        new_yl = new_yl[1:]

    return new_xu, new_yu, new_xl, new_yl


# Saves the coordines x, y into a file
def save_file(x, y, name):
    file = open(name, 'w')
    for i in range(len(x)):
        file.write(str(x[i]) + ' ')
        file.write(str(y[i]) + '\n')
    file.close


# To copy file from one directory to another
def copy_item(from_path, to_path, item):
    from_path = from_path + item
    to_path = to_path + item
    shutil.copyfile(from_path, to_path)


# To move file from one directory to another
def move_item(from_path, to_path, item):
    from_path = from_path + item
    to_path = to_path + item
    shutil.copyfile(from_path, to_path)
    os.remove(item)


# Plots airfoil with inputs x coordinates, y coordinates and title
def plotting(x, y, title):
    plt.figure()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.plot(x, y, color='black')
    plt.show


# Gives new coordinates with inputs airfoil .dat file name and number of points required on top and bottom half of airfoil
def new_foil(foil, pts):
    (x, y) = extract.coordinates(foil + '.dat')
    (xu, yu, xl, yl) = xtra_pts(x, y, pts)
    x = xu + xl
    y = yu + yl
    for f in os.listdir(code_path):
        if f == foil + '.dat':
            os.remove(foil + '.dat')
    save_file(x, y, foil + '.dat')
    return x, y


# Gives cp values
def cp_fun(foil_name, Re, Mach, N_crit, Alpha):
    for f in os.listdir(code_path):
        if f == 'Cp_' + foil_name + '_(' + str(Alpha) + ')' + '.txt':
            os.remove('Cp_' + foil_name + '_(' + str(Alpha) + ')' + '.txt')
    cp = xfoil.cp_oper(foil_name, Re, Mach, N_crit, Alpha)
    return cp


# Gives polar values
def polar_fun(foil_name, Re, Mach, N_crit, Alpha):
    for f in os.listdir(code_path):
        if f == 'Polar_' + foil_name + '_(' + str(Alpha) + ')' + '.txt':
            os.remove('Polar_' + foil_name + '_(' + str(Alpha) + ')' + '.txt')
    alpha, cl, cd, cdp, cm = xfoil.polar_oper(foil_name, Re, Mach, N_crit, Alpha)
    return alpha, cl, cd, cdp, cm


###########################################################################################################################



###########################################################################################################################

#################################################### THE CODE #############################################################
xfoil = xfoil()
extract = extract()

###########################################################################################################################

############################################# REMOVING UNNECESSARY FILES ##################################################

###########################################################################################################################
