import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

from utils.input_output import sort_file
from utils.plot_functions import plot_iso
def plot_folder_shifted_custome(foldername, label_list):
    filenames = sort_file(foldername)
    os.chdir(foldername)
    cmap = plt.get_cmap('tab10')
    line2d_list = []
    from utils.input_output import shift_data_lab
    for i in range(len(filenames)):
        print(len(filenames))
        file = filenames[i]
        area, pressure = shift_data_lab(file)
        legend = label_list[i]
        c = cmap(i)
        line = plot_iso(area, pressure, legend, c)
        line2d_list.append(line)
    plt.show()
    return line2d_list

folder = '/Users/rachel/Isotherms/plotting'
label_list = ['water', '0.1mM KI', '0.3mM KI', '0.6mM KI', '1.25mM KI']
lines = plot_folder_shifted_custome(folder, label_list)

from utils.isotherm_library import ion_dic
key = 'I'
conc_list = np.array(ion_dic[key]['conc_list'])
folder1 = ion_dic[key]['folder']  ##folder location is in isotherm library
from utils.math_functions import kink_list_df_fit
kink_list = kink_list_df_fit(folder1)

from utils.math_functions import langmuir_iso
from utils.math_functions import fit_langmuir
xdata = np.linspace(0, max(conc_list), 100)
pmax, kd = fit_langmuir(conc_list, kink_list, 2.371)
ydata = langmuir_iso(xdata, pmax, kd, 2.371)


fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(6, 8))
ax_top.text(0.02, 0.95, '(a)', transform=ax_top.transAxes, fontsize=12, va='top', ha='left')
ax_bottom.text(0.02, 0.95, '(b)', transform=ax_bottom.transAxes, fontsize=12, va='top', ha='left')

i = 0
for line in lines:
    ax_top.plot(line.get_xdata(), line.get_ydata(), label=label_list[i])
    i+=1
ax_top.legend()
ax_top.set_xlim(5, 60)
ax_top.set_xlabel('area/molecule ($\AA^2$)')
ax_top.set_ylabel('pressure (mN/m)')

ax_bottom.scatter(conc_list, kink_list, color='royalblue')
ax_bottom.plot(xdata, ydata, color = 'tab:blue')
ax_bottom.set_xlabel(r'$c_{salt}$')
ax_bottom.set_ylabel(r'$\Pi_t$ (mN/m)')
s = r'$\Pi_{max}$ = ' + str(round(pmax, 2)) + r'mN/m, $k_d$ = ' + str(round(kd, 3)) + 'mM'
ax_bottom.text(0.9, 5, s, horizontalalignment='center', verticalalignment='center')

fig.tight_layout()

plt.savefig('/Users/rachel/NU research/paper_fig1.png')
fig.show()





