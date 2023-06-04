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
    plt.scatter(area, pressure, label = legend, color = c, s = 0.3)
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



#Come back here if plot_kink not work for cutted data
def plot_kink_fig(foldername, conc_list):
    from utils.math_functions import kink_list, kink_list_cutted_fit, kink_list_df_fit
    kink_list = kink_list_df_fit(foldername)
    print(kink_list)
    print(conc_list)
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
    pmax, kd = fit_langmuir(concentration, kink_pressure)
    s = 'pmax = ' + str(round(pmax, 2)) + ', kd = ' + str(round(kd, 3))
    print(kd)
    plt.text(concentration[-1] - concentration[-1] / 2.5, kink_pressure[-1] + 1, s)
    plt.plot(concentration, langmuir_iso(concentration, pmax, kd))
    plt.savefig(title + '_langmuir_fit.png')
    plt.show()












