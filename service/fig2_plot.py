import numpy as np
import matplotlib.pyplot as plt
from utils.math_functions import kink_list_df_fit
from utils.math_functions import fit_langmuir
from utils.math_functions import langmuir_iso

from utils.isotherm_library import ion_dic

conc_lists = []
kink_pressures_list = []
ion_of_interest = ['F', 'Cl', 'Br', 'I', 'NO3', 'ClO4', 'SCN']
#ion_of_interest = ['I']
for key in ion_of_interest:
    if key in ion_dic:
        folder = ion_dic[key]['folder']
        kink_pressures = kink_list_df_fit(folder)
        kink_pressures_list.append(kink_pressures)
        conc_list = ion_dic[key]['conc_list']
        conc_lists.append(conc_list)
        # print(folder)
        # print(kink_pressures)
        # print(conc_list)


fig, ax = plt.subplots()
cmap = plt.get_cmap('tab10')
kd_list = []
pmax_list = []
for i in range(len(ion_of_interest)):
    print(ion_of_interest[i])
    conc_list = conc_lists[i]
    kink_list = kink_pressures_list[i]
    print(len(kink_list))
    print(len(conc_list))
    ax.scatter(conc_list, kink_list, color = cmap(i), label = ion_of_interest[i])

    pmax, kd = fit_langmuir(conc_list, kink_list, p0 = 2.371)
    kd_list.append(kd)
    pmax_list.append(pmax)
    xdata = np.linspace(0, max(conc_list), 100)
    ydata = langmuir_iso(xdata, pmax, kd, p0 = 2.371)
    ax.plot(xdata, ydata, color = cmap(i))

ax.set_xlim(0, 2.2)
ax.set_xlabel(r'$c_{salt}$ (mM)')
ax.set_ylabel(r'$\Pi_t$ (mN/m)')
ax.legend()
plt.savefig('/Users/rachel/NU research/paper_fig2.png')
fig.show()

langmuir_fit_result = np.column_stack((ion_of_interest, pmax_list, kd_list))
print(langmuir_fit_result)
file_path = '/Users/rachel/NU research/langmuir fit paras.txt'
np.savetxt(file_path, langmuir_fit_result, fmt = '%s', header='ion pmax kd', comments='')





