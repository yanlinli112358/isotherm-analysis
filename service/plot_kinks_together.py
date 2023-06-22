import matplotlib.pyplot as plt

from utils.plot_functions import plot_single_kink
import os
main_folder = '/Users/rachel/Isotherms/'
os.chdir(main_folder)

folder_list = ['KF_ODA_2023_4', 'KNO3_ODA_2023_6', 'KCl_ODA_2023_1', 'KBr_ODA_2023_1', 'KClO4_ODA_2023_6',
               'KI_ODA_2023_1', 'KSCN_ODA_2023_6']
conc_list = []

from utils.isotherm_library import ion_dic
for folder in folder_list:
    for key in ion_dic:
        if key == folder[1: -11]:
            print('key = ' + key)
            conc = ion_dic[key]['conc_list']
            conc_list.append(conc)
            print(conc_list[-1])

plt.figure()
plt.xlim(0, 2)
plt.ylim(0, 60)
for i in range(len(folder_list)):
    print(i)
    plot_single_kink(folder_list[i], conc_list[i], label=folder_list[i])
plt.legend()
plt.savefig(os.path.join('Plots','potassium salts 0-1mM.png' ))
plt.show()

