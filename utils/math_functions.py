import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from utils.input_output import get_data_lab, sort_file

#piecewise function
def p(a, p0, p1, p2, a0, a1, a2):
    # p_values: list of transition values in  order of (p0, p1, p2)
    # a_values: list of transition values in order of (a0, a1, a2)
    c1 = (p1 - p0) / (a1 - a0)
    b1 = p1 - c1 * a1
    c2 = (p2 - p1) / (a2 - a1)
    b2 = p2 - c2 * a2

    cond_list = [a < a2, (a2 <= a) & (a < a1), (a1 <= a) & (a < a0), a >= a0]
    func_list = [p2, lambda a: c2 * a + b2, lambda a: c1 * a + b1, p0]

    pressure = np.piecewise(a, cond_list, func_list)
    return pressure

def p_partial(a, p0, p1, a0, a1, a2):
    c1 = (p1-p0)/(a1-a0)
    b1 = p1 - c1 * a1
    c2 = (30-p1)/(a2-a1)
    b2 = p1 - c2 * a1
    cond_list = [a < a1, (a1 <= a) & (a < a0), a > a0]
    func_list = [lambda a: c2 * a + b2, lambda a: c1 * a + b1, p0]

    pressure = np.piecewise(a, cond_list, func_list)
    return pressure

def find_kink(filename):
    area_per_m, pressure = get_data_lab(filename)
    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(p, area_per_m, pressure, p0=(0, 10, 60, 22, 20, 15))
    kink_pressure = popt[1] - popt[0]
    return kink_pressure

def find_min_area(filename):
    area_per_m, pressure = get_data_lab(filename)
    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(p, area_per_m, pressure, p0=(0, 10, 60, 22, 20, 15))
    min_area = popt[-1]
    return min_area

from scipy.optimize import curve_fit
def fit_piecewise(filename):
    area_per_m, pressure = get_data_lab(filename)
    popt, pcov = curve_fit(p, area_per_m, pressure, p0=(0, 10, 60, 22, 20, 15))
    return popt

def fit_piecewise_partial(filename):
    area, p = get_data_lab(filename)
    p_cutted = []
    a_cutted = []
    i = 0
    print(filename)
    while p[i] < 30:
        p_cutted.append(p[i])
        a_cutted.append(area[i])
        i += 1
    popt, pcov = curve_fit(p_partial, a_cutted, p_cutted, p0 = (0, 10, 23, 21, 19))
    return popt

def find_kink_partial(filename):
    popt = fit_piecewise_partial(filename)
    return popt[2] - popt[0]

def find_collapse_area(filename):
    area_per_m, pressure = get_data_lab(filename)
    dpda = np.gradient(pressure, area_per_m)
    threshold = 10
    change_points = np.where((np.diff(dpda) > threshold))[0] + 1
    min_area = area_per_m[change_points[-1]]
    return min_area

def find_area_at_pressure(target_pressure, filename):
    from utils.input_output import shift_data_lab
    area, pressure = shift_data_lab(filename)
    area_index = np.argwhere(pressure >= target_pressure)
    solution = area[np.min(area_index)]
    return solution

def kink_list(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    kink_list = []
    for i in range(len(filenames)):
        kink_p = find_kink(filenames[i])
        kink_list.append(kink_p)
    os.chdir(Path(os.getcwd()).parent)
    return kink_list

def kink_list_cutted_fit(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    kink_list = []
    for i in range(len(filenames)):
        kink_p = find_kink_partial(filenames[i])
        kink_list.append(kink_p)
    os.chdir(Path(os.getcwd()).parent)
    return kink_list



## derivative method:
def derivative(x, y):
    dx = np.gradient(x)
    dy = np.gradient(y)
    dy_dx = dy / dx
    return dy_dx

def find_kink_df(filename):
    area, p = get_data_lab(filename)
    i = 0
    area_cutted = []
    p_cutted = []
    while (p[i] < 0.2):
        i += 1
    while (p[i] < 50 or p[i] < max(p)):
        p_cutted.append(p[i])
        area_cutted.append(area[i])
        i += 1
    dp_da = derivative(area_cutted, p_cutted)
    j = 0
    p_kink = p_cutted[j]
    while ((dp_da[j] > -10)or (dp_da[j+1] > -10)):
        p_kink = p_cutted[j]
        #a_kink = area_cutted[j + 1]
        j = j + 1
    return p_kink

def kink_list_df_fit(foldername):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    kink_list = []
    for i in range(len(filenames)):
        print(filenames[i])
        kink_p = find_kink_df(filenames[i])
        kink_list.append(kink_p)
    os.chdir(Path(os.getcwd()).parent)
    return kink_list

##fit with Lagmuir isotherm
def langmuir_iso(c, pmax, kd):
    return pmax * c / (kd + c)

def fit_langmuir(concentration, kink_pressure):
    popt, pcov = curve_fit(langmuir_iso, concentration, kink_pressure, p0 = (30, 0.5))
    pmax = popt[0]
    kd = popt[1]
    return pmax, kd








