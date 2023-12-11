'''
This file models ionization fraction of monolayer (x) with monovalent
salt using size modified PB model
'''
import numpy as np
import matplotlib.pyplot as plt

pH = 5.7
pKa = 10.5
electron_charge = 1.602e-19
ep0 = 8.85e-12
epr = 78.5
kB = 1.38e-23
T = 279.5 + 20
avo_num = 6.022e23
A = 20

print(electron_charge/np.sqrt(8*ep0*epr*kB*T))
print(electron_charge**2 / (4*epr*ep0*kB * T))


def get_ionization_frac(a, c_ion, pH, pKa):
    #a = ion size, c_bulk = bulk concentration of ion
    #LHS
    def g(x, pH, pKa):
        return np.log10((1-x)/x) - pH + pKa

    def f(a, x, c_ion, pH, pKa):
        c_bulk = c_ion + 10 ** (-pH)
        phi0 = 2 * c_bulk * a**3
        in_exp = 22.3*2 * x**2 * a**3 / A**2
        in_sinh = np.sqrt(1/(2*phi0) * np.exp(in_exp) - 1/(2*phi0))
        return 0.87 * np.arcsinh(in_sinh)

    def objective(x):
        return abs(g(x, pH, pKa) - f(a, x, c_ion, pH, pKa))

    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return res.x

print(get_ionization_frac(1.5, 1e-1, pH, pKa))


ion_size_list = [1.7, 2.2, 2.4]
label_list = ['Cl', 'I', 'ClO4']
plt.figure()
concentration_list = np.linspace(5e-5, 7.5e-4)
i = 0
for a in ion_size_list:
    x_list = []
    for c_ion in concentration_list:
        x_list.append(get_ionization_frac(a, c_ion, pH, pKa))
    x_list = np.array(x_list)
    plt.plot(concentration_list, x_list, label = label_list[i])
    i = i+1
c_data = 1e-3* np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
y_data = 25 * np.array([0.00335, 6.01e-3, 7.75e-3, 1.26e-2, 1.31e-2, 1.40e-2, 0.0148, 1.47e-2])
c_cl = [0.4e-3, 0.5e-3]
y_cl = [0.007102353*20, 0.0077*20]
y_clo4 = [0.009355101*26, 1.07e-2*26]

plt.scatter(c_cl, y_cl, label = 'XF data chlorine')
plt.scatter(c_cl, y_clo4, label = 'XF data perchloride')
plt.scatter(c_data, y_data, label = 'XF data iodine')

from utils.Gouy_chapmann_model import ion_frac
ion_frac_list = []
for c_ion in concentration_list:
    ion_frac_list.append(ion_frac(c_ion, pH, pKa, A))
plt.plot(concentration_list, ion_frac_list, linestyle='dashed', label = 'PB model')

plt.xlabel('bulk ion concentration (M)')
plt.ylabel('ionization fraction (AA^-2)')
plt.ylim(0, 1)
plt.legend()
plt.show()

plt.figure()
concentration_list = np.logspace(-10, -1, 1000) #concentration list in log space
i = 0
for a in ion_size_list:
    x_list = []
    for c_ion in concentration_list:
        x_list.append(get_ionization_frac(a, c_ion, pH, pKa))
    x_list = np.array(x_list)
    plt.semilogx(concentration_list, x_list, label = label_list[i])
    i = i+1
from utils.Gouy_chapmann_model import ion_frac
ion_frac_list = []
for c_ion in concentration_list:
    ion_frac_list.append(ion_frac(c_ion, pH, pKa, A))
plt.plot(concentration_list, ion_frac_list, linestyle='dashed', label = 'PB model')

plt.xlabel('bulk ion concentration (M)')
plt.ylabel('ionization fraction (AA^-2)')
plt.ylim(0, 1)
plt.legend()
plt.show()