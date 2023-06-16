import os

import matplotlib.pyplot as plt
import numpy as np
p0 = 3.07

main_folder = '/Users/rachel/Isotherms/'
os.chdir(main_folder)
ion = 'F'
folder1 = 'KF_ODA_2023_4'

from utils.isotherm_library import ion_dic
for key in ion_dic:
    if key==ion:
        conc_list = ion_dic[key]['conc_list']
print(conc_list)

from utils.plot_functions import plot_folder_shifted, plot_folder

#plot_folder_shifted(folder1)
plot_folder(folder1)

'''
from utils.math_functions import find_area_at_pressure
from utils.input_output import sort_file
from utils.math_functions import find_kink
#filenames = os.listdir(os.path.join(main_folder, folder1))
filenames = sort_file(os.path.join(main_folder, folder1))
area_list = []
kink_list = []
for i in range(len(filenames)):
    print(filenames[i])
    area = find_area_at_pressure(7, filenames[i])
    kink_p = find_kink(filenames[i])
    area_list.append(area)
    kink_list.append(kink_p)
print(area_list)

conc_list = [0.01, 0.025, 0.05, 0.075, 0.1, 0.125]
kink_list = [3.75, 6.25, 8.25, 10.5, 12.5, 13]
plt.figure()
plt.scatter(conc_list, kink_list)
plt.xlabel('concentration(mM)')
plt.ylabel('transition pressure(dynes)')
plt.title('KSCN')
plt.savefig('KSCN_kink_pressure.png')
plt.show()
'''
conc_list_F = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.25, 1.5, 2, 3, 4, 5, 7, 10, 15]
conc_list_Br = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.5, 2]
conc_list_I = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.25]
conc_list_SO4 = [0, 0.0025, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.05, 0.075, 0.1]
conc_list_Cl = [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 0.817, 1.10, 1.5, 2.15, 2.69, 3, 5]
conc_list_NO3 = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75]
conc_list_HCO3 = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
# from utils.plot_functions import plot_kink_fig
# plot_kink_fig(folder1, conc_list)


from utils.plot_functions import plot_kink_fig
kink_list = plot_kink_fig(folder1, conc_list)
print(kink_list)

from utils.plot_functions import plot_langmuir_fit
plot_langmuir_fit(np.array(conc_list), np.array(kink_list), title=ion)

from utils.plot_functions import plot_langmuir_fit_linear
plot_langmuir_fit_linear(np.array(conc_list), np.array(kink_list), title=ion)



