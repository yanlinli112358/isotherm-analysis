import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

conc_list = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75])
cov_list = np.array([0.071, 0.15, 0.203, 0.328, 0.362, 0.378, 0.421, 0.410])

from utils.math_functions import langmuir_iso
def langmuir_iso_fix_kd(c, pmax):
    return langmuir_iso(c, pmax, 0.1997, 0)

popt, pcov = curve_fit(langmuir_iso_fix_kd, conc_list, cov_list, p0=0.5,
                       bounds=(0.4, 1))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (6, 8))
path = '/Users/rachel/NSLS_II_beamtrips/313179_dutta_shared/fig3 selected'
from utils.input_output import sort_file
files = sort_file(path)
print(files)
i = 0
label_list = ['0.1mM KI', '0.2mM KI', '0.3mM KI']
for file in files:
    f = open(os.path.join(path, file), 'r')
    line = f.readline()
    qz_list = []
    intensity_list = []
    err_list = []
    while line:
        data = line.split()
        qz_list.append(float(data[0]))
        intensity_list.append(float(data[1]))
        err_list.append(float(data[2]))
        line = f.readline()
    from matplotlib.ticker import ScalarFormatter
    ax1.errorbar(qz_list, intensity_list, yerr = err_list, fmt = 'o', markersize=4, label = label_list[i])
    i += 1

ax1.legend()
ax1.set_xlim(0, 0.065)
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-3, 2))
ax1.set_ylim(0, 0.0009)
ax1.yaxis.set_major_formatter(formatter)
ax1.set_xlabel('Qz')
ax1.set_ylabel('Fluorescence intensity (a.u.)')


pmax = popt[0]
print(pmax)
ax2.scatter(conc_list, cov_list)
xdata = np.linspace(0, 0.8, 100)
ax2.plot(xdata, langmuir_iso_fix_kd(xdata, pmax))
ax2.set_xlabel(r'$c_{salt}$ (mM)')
ax2.set_ylabel('ion/headgroup ratio')

ax1.text(0.02, 0.95, '(a)', transform=ax1.transAxes, fontsize=12, va='top', ha='left')
ax2.text(0.02, 0.95, '(b)', transform=ax2.transAxes, fontsize=12, va='top', ha='left')

plt.savefig('/Users/rachel/NU research/paper_fig3.png')
plt.show()
