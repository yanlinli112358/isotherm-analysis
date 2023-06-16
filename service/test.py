import matplotlib.pyplot as plt

from utils.plot_functions import plot_folder, plot_folder_shifted
from utils.input_output import get_data_lab
import os
os.chdir('/Users/rachel/Isotherms')
folder = '0.1mM potassium salts'
plot_folder(folder)

from utils.math_functions import find_kink_df
from utils.plot_functions import plot_kink_fig, plot_single_kink
ion_list = ['water', 'F', 'HCO3', 'NO3', 'Cl', 'Br', 'I']
kink_list = plot_kink_fig(folder, ion_list)

ion_size_list = [0, 0.124, 0.156, 0.177, 0.18, 0.198, 0.225]
#ion_size_list = [0, 0.156, 0.177, 0.18, 0.198, 0.225]
plt.scatter(ion_list, ion_size_list, label = 'ionic radii')
plt.xlabel('ions')
plt.ylabel('ion radii(nm)')
plt.show()
