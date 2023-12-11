'''this file models the Gouy-Chapmann in terms of HX- (hydrogen + an
anion X-) binding to NH2 instead of X- binding to NH3

Parameters in the model:
pH: pH of the bulk solution
pKA: pKA of the molecule ODA
pKd: pK (log dissociation) of the group HX- to NH2
c_ion: bulk concentration of the ion X- in M
A: area per ODA head, assume to be 20 A^2 across the model, not defined as parameter
'''
import numpy as np
import matplotlib.pyplot as plt

pH = 5.7
pKA = 10.5

def x_ion_expression(x_H, c_ion, pH, pKA, pKd):
    power = pH - pKA - pKd - np.log10(c_ion)
    return (1 - x_H) / (np.power(10, power) + 1)

def get_x_H(c_ion, pH, pKA, pKd):
    def g(c_ion, pH): #LHS
        c_total = c_ion + 10 ** (-pH)
        return 20 * np.sqrt(c_total) #assume A = 20, 134/20 = 6.7

    def f(x_H, c_ion, pH, pKA, pKd): #RHS
        x_ion = x_ion_expression(x_H, c_ion, pH, pKA, pKd)
        in_log = (1 - x_H - x_ion) / x_H
        in_sinh = (np.log10(in_log) - pH + pKA) / 0.87

        numerator = 134 * x_H
        denominator = np.sinh(in_sinh)
        return numerator / denominator

    def objective(x_H):
        return abs(g(c_ion, pH) - f(x_H, c_ion, pH, pKA, pKd))

    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='Bounded')
    return res.x

def xH_list(conc_list, pH, pKA, pKd):
    ion_frac_list = []
    for c in conc_list:
        xH_frac = get_x_H(c, pH, pKA, pKd)
        ion_frac_list.append(xH_frac)
    return ion_frac_list

def x_ion_list(conc_list, pH, pKA, pKd):
    x_ion_list = []
    x_H_list = xH_list(conc_list, pH, pKA, pKd)
    for i in range(len(x_H_list)):
        x_ion = x_ion_expression(x_H_list[i], conc_list[i], pH, pKA, pKd)
        x_ion_list.append(x_ion)

    return x_ion_list

conc_list = np.linspace(1e-5, 1e-3, 1000)

plt.figure()
plt.xlabel('concentration(M)')
plt.ylabel('monolayer ionization fraction')
pKd_list = [-0.249, -0.057, 0.228, 0.318, 0.538, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'ClO4', 'SCN', 'I']
for i in range(len(pKd_list)):
    xH_frac = xH_list(conc_list, pH, pKA, pKd_list[i])
    plt.plot(conc_list, xH_frac, label = label_list[i])
plt.legend()
plt.savefig('/Users/rachel/NU research/graphs/monolayer ionization fraction GC_model2')
plt.show()

plt.figure()
plt.xlabel('concentration(M)')
plt.ylabel('ion adsorption fraction')
pKd_list = [-0.249, -0.057, 0.228, 0.318, 0.538, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'ClO4', 'SCN', 'I']
for i in range(len(pKd_list)):
    xion_frac = x_ion_list(conc_list, pH, pKA, pKd_list[i])
    plt.plot(conc_list, xion_frac, label = label_list[i])
plt.legend()
plt.savefig('/Users/rachel/NU research/graphs/ion adsorption fraction GC_model2')
plt.show()


plt.figure()
plt.xlabel('concentration(M)')
plt.ylabel('Remaining deprotonated NH2 fraction')
pKd_list = [-0.249, -0.057, 0.228, 0.318, 0.538, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'ClO4', 'SCN', 'I']
for i in range(len(pKd_list)):
    xion_frac = x_ion_list(conc_list, pH, pKA, pKd_list[i])
    xH_frac = xH_list(conc_list, pH, pKA, pKd_list[i])
    nh2_frac = 1 - np.array(xH_frac) - np.array(xion_frac)
    plt.plot(conc_list, nh2_frac, label = label_list[i])
plt.legend()
plt.savefig('/Users/rachel/NU research/graphs/remaining NH2 fraction GC_model2')
plt.show()






