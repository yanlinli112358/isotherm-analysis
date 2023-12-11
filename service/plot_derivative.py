import numpy as np
import matplotlib.pyplot as plt
import os
main_folder = '/Users/rachel/Isotherms/KSCN_ODA_2023_6'
os.chdir(main_folder)
filename = '1mM_KSCN.txt'
def derivative(x, y):
    dx = np.gradient(x)
    dy = np.gradient(y)
    dy_dx = dy / dx
    return dy_dx

def plot_df(filename):
    from utils.input_output import get_data_lab
    area, p = get_data_lab(filename)
    area_cutted = []
    p_cutted = []
    i = 0
    while (p[i] < 0.2):
        i += 1
    while (p[i] < 50):
        p_cutted.append(p[i])
        area_cutted.append(area[i])
        i += 1
    dp_da = derivative(area_cutted, p_cutted)
    dp_da2 = derivative(area_cutted, dp_da)
    plt.scatter(area_cutted, dp_da)
    plt.show()

plot_df(filename)

from utils.math_functions import find_kink_df
p_kink = find_kink_df(filename)
print(p_kink)

def plot_cutted_region(filename):
    from utils.input_output import get_data_lab
    area, p = get_data_lab(filename)
    area_cutted = []
    p_cutted = []
    i = 0
    while (p[i] < 0.2):
        i += 1
    while (p[i] < 50):
        p_cutted.append(p[i])
        area_cutted.append(area[i])
        i += 1
    plt.plot(area_cutted, p_cutted)
    plt.show()

plot_cutted_region(filename)
from utils.math_functions import check_slope
check_slope()









