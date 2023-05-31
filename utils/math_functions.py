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

def p_partial(a, p0, a0, p1, a1, c2, b2):
    c1 = (p1-p0)/(a1-a0)
    b1 = p1 - c * a1
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

def fit_piecewise(filename):
    area_per_m, pressure = get_data_lab(filename)
    from scipy.optimize import curve_fit
    popt, pcov = curve_fit(p, area_per_m, pressure, p0=(0, 10, 60, 22, 20, 15))
    return popt


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









