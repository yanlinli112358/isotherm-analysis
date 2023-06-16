import matplotlib.pyplot as plt

from utils.plot_functions import plot_single_kink
import os
main_folder = '/Users/rachel/Isotherms/'
os.chdir(main_folder)
conc_list_F = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.25, 1.5, 2, 3, 4, 5, 7]
conc_list_Br = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.5, 2]
conc_list_I = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.25]
conc_list_SO4 = [0, 0.0025, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.05, 0.075, 0.1]
conc_list_Cl = [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 0.817, 1.10, 1.5, 2.15, 2.69, 3, 5]
conc_list_NO3 = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75]

folder_list = ['KF_ODA_2023_4','KNO3_ODA_2023_6', 'KCl_ODA_2023_1', 'KBr_ODA_2023_1', 'KI_ODA_2023_1']
conc_list = [conc_list_F, conc_list_NO3, conc_list_Cl, conc_list_Br, conc_list_I]

plt.figure()
plt.xlim(0, 1)
plt.ylim(0, 60)
for i in range(len(folder_list)):
    plot_single_kink(folder_list[i], conc_list[i], label=folder_list[i])
plt.legend()
plt.savefig(os.path.join('Plots','potassium salts 0-1mM.png' ))
plt.show()

