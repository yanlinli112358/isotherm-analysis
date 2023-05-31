import os.path
from pathlib import Path

import matplotlib.pyplot as plt
from utils.input_output import get_data_lab, sort_file
def plot_piecewise(a, popt): #a:area, popt: list of parameter
    from math_functions import p
    p0, p1, p2, a0, a1, a2 = popt
    pressure = p(a, p0, p1, p2, a0, a1, a2)
    plt.plot(a, pressure)

def plot_file(filename, legend, c):
    area_per_m, pressure = get_data_lab(filename)
    plt.plot(area_per_m, pressure, label=legend, color = c)
    plt.legend()
    return None

def plot_iso(area, pressure, legend, c):
    plt.plot(area, pressure, label = legend, color = c)
    plt.legend()

def plot_folder(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    cmap = plt.get_cmap('viridis')
    for i in range(len(filenames)):
        from utils.input_output import shift_data_lab
        file = filenames[i]
        area, pressure = get_data_lab(file)
        legend = file[:-4]
        c = cmap(i/len(filenames))
        plot_iso(area, pressure, legend, c)
    plt.grid()
    plt.xlabel('area (Angstrom^2)')
    plt.ylabel('pressure')
    plt.savefig('isotherms')
    plt.show()
    os.chdir(Path(os.getcwd()).parent)

def plot_folder_shifted(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    cmap = plt.get_cmap('viridis')
    for i in range(len(filenames)):
        from utils.input_output import shift_data_lab
        file = filenames[i]
        area, pressure = shift_data_lab(file)
        legend = file[:-4]
        c = cmap(i/len(filenames))
        plot_iso(area, pressure, legend, c)
    plt.grid()
    plt.xlabel('area (Angstrom^2)')
    plt.ylabel('pressure')
    plt.savefig('shifted_isotherms')
    plt.show()
    os.chdir(Path(os.getcwd()).parent)

def plot_kink_fig(foldername, conc_list):
    from utils.math_functions import kink_list
    kink_list = kink_list(foldername)
    plt.scatter(conc_list, kink_list)
    plt.xlabel('concentration(mM)')
    plt.ylabel('transition pressure(dynes)')
    plt.savefig('kink_pressure')
    plt.show()







