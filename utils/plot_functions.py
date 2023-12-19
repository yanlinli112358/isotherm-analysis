import os.path
from pathlib import Path
import numpy as np
p0 = 2.371

import matplotlib.pyplot as plt
from utils.input_output import get_data_lab, sort_file, write_area_pressure
def plot_piecewise(a, popt): #a:area, popt: list of parameter
    from math_functions import p
    p0, p1, p2, a0, a1, a2 = popt
    pressure = p(a, p0, p1, p2, a0, a1, a2)
    plt.plot(a, pressure)

def plot_file(filename, legend, c):
    area_per_m, pressure = get_data_lab(filename)
    plt.plot(area_per_m, pressure, label=legend, color = c)
    plt.legend()
    return area_per_m, pressure

def plot(filename):
    area_per_m, pressure = get_data_lab(filename)
    plt.plot(area_per_m, pressure)
    plt.show()
    return area_per_m, pressure

def plot_iso(area, pressure, legend, c):
    fig, = plt.plot(area, pressure, label = legend, color = c)
    return fig

def plot_folder(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    cmap = plt.get_cmap('tab10')
    for i in range(len(filenames)):
        from utils.input_output import shift_data_lab
        file = filenames[i]
        area, pressure = get_data_lab(file)
        legend = file[:-4]
        c = cmap(i)
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

def plot_folder_calibrated(foldername):
    filenames = sort_file(foldername)
    for file in filenames:
        print(file)
        area = []
        pressure = []
        filepath = os.path.join(foldername, file)
        f = open(filepath, 'r')
        line = f.readline()
        while line:
            data = line.split()
            area.append(float(data[0]))
            pressure.append(float(data[1]))
            line = f.readline()
        plt.plot(area, pressure, label = file[:-4])
    plt.xlabel(r'area per molecule ($\AA^2$)')
    plt.ylabel('pressure (mN/m)')
    plt.legend()
    savename = os.path.join(foldername + 'calibrated_isotherm.png')
    plt.savefig(savename)
    plt.show()


#Come back here if plot_kink not work for cutted data
def plot_kink_fig(foldername, conc_list):
    from utils.math_functions import kink_list, kink_list_df_fit
    kink_list = kink_list_df_fit(foldername)
    plt.scatter(conc_list, kink_list)
    plt.xlabel('concentration(mM)')
    plt.ylabel('transition pressure(dynes)')
    plt.savefig(os.path.join(foldername, 'kink_pressure'))
    plt.show()
    return kink_list


def plot_langmuir_fit(concentration, kink_pressure, title):
    from utils.math_functions import langmuir_iso, fit_langmuir
    plt.xlabel('concentration(mM)')
    plt.ylabel('pressure(dynes)')
    plt.ylim(0, max(kink_pressure) + 3)
    plt.title(title)
    plt.scatter(concentration, kink_pressure)
    pmax, kd = fit_langmuir(concentration, kink_pressure, p0)
    s = 'pmax = ' + str(round(pmax, 2)) + ', kd = ' + str(round(kd, 3))
    plt.text(concentration[-1] - concentration[-1] / 2.5, kink_pressure[-1] + 1, s)
    plt.plot(concentration, langmuir_iso(concentration, pmax, kd, p0))
    plt.savefig(os.path.join('Plots', title + '_langmuir_fit.png'))
    plt.show()

def plot_single_kink(foldername, conc_list, label):
    #plot function to be called to plot several kinks together
    from utils.math_functions import kink_list, kink_list_df_fit
    kink_list = kink_list_df_fit(foldername)
    plt.plot(conc_list, kink_list, label = label, marker='o')
    return kink_list

def plot_langmuir_fit_linear(concentration, kink_pressure, title):
    from utils.math_functions import fit_langmuir_linear, langmuir_iso_linear
    plt.xlabel('concentration(mM)')
    plt.ylabel('pressure(dynes)')
    plt.ylim(0, max(kink_pressure) + 3)
    plt.title(title)
    plt.scatter(concentration, kink_pressure)
    plt.show()
    pmax, kd, b = fit_langmuir_linear(concentration, kink_pressure, p0)
    s = 'pmax = ' + str(round(pmax, 2)) + ', kd = ' + str(round(kd, 3)) + ',b = ' + str(round(b, 3))
    plt.text(concentration[-1] - concentration[-1] / 2, kink_pressure[-1] + 1, s) #position of text
    plt.plot(concentration, langmuir_iso_linear(concentration, pmax, kd, b, p0))
    plt.savefig(os.path.join('Plots', title + '_langmuir_fit_linear_term.png'))
    plt.show()


def plot_shift_iso_area(filename, shift_scale, legend, c):
    area, pressure = get_data_lab(filename)
    shifted_area = np.array(area) * shift_scale
    savename = filename + '_shifted_scale_' + str(shift_scale) + '.txt'
    write_area_pressure(savename, shifted_area, pressure)
    plot_iso(shifted_area, pressure, legend=filename, c = c)
    plt.show()
    return shifted_area, pressure








