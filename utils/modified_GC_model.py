import numpy as np
import matplotlib.pyplot as plt
import sympy
from sympy import symbols, Eq, solve, nsolve
from sympy import log, sinh, Pow, sqrt, asinh


# Rest of your code...
pH = 5.7
pKa = 10.5
electron_charge = 1.602e-19
ep0 = 8.85e-12
epr = 78.5
kB = 1.38e-23
T = 279.5 + 20
avo_num = 6.022e23
#c_ion = 1e-3
#c_ion = concentration of ion in M

def get_x_total(c_ion, pH, pKa):
    #g = LHS of eq(4) in 'Salt promotes protonation'
    def g(c_ion, pH):
        return np.sqrt(c_ion + 10 ** (-pH))
    #f = RHS of eq(4)
    def f(pH, pKa, x):
        temp = (np.log10((1 - x) / x) - pH + pKa) / 0.87
        return 134 * x / (20 * np.sinh(temp)) ## ODA area = 20
    #objective = abs(LHS-RHS)
    def objective(x):
        return abs(g(c_ion, pH) - f(pH, pKa, x))
    #res is the solutions that minimize the difference b/w LHS and RHS
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')

    return res.x

def get_x_ion(c_ion, pH, pKa, pK_ion):
    x_total = get_x_total(c_ion, pH, pKa)
    def g(c_ion, x_ion, pH):
        x_proton = x_total - x_ion
        return 134 * x_proton / 20 / np.sqrt(c_ion + 10**(-pH)) #A = 20

    def f(c_ion, x_ion, pK_ion):
        x_proton = x_total - x_ion
        term1 = -pK_ion
        term2 = np.log10(x_ion/x_proton)
        term3 = -np.log10(c_ion)
        return np.sinh((term1 + term2 + term3)/0.87)

    def objective(x_ion):
        return abs(g(c_ion, x_ion, pH) - f(c_ion, x_ion, pK_ion))

    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, x_total), method='bounded')
    return res.x

def get_x_proton(c_ion, pH, pKa, pK_ion):
    x_total = get_x_total(c_ion, pH, pKa)
    x_ion = get_x_ion(c_ion, pH, pKa, pK_ion)
    return x_total - x_ion

def ionization_frac(conc_list, pH, pKa):
    ion_frac = []
    for c in conc_list:
        x = get_x_total(c, pH, pKa)
        ion_frac.append(x)
    return ion_frac

def adsorb_frac(conc_list, pH, pKa, pK_ion):
    ion_frac = []
    for c in conc_list:
        x = get_x_ion(c, pH, pKa, pK_ion)
        ion_frac.append(x)
    return ion_frac

def potential(c_ion, pH, pKa, pK_ion):
    x_charged = get_x_proton(c_ion, pH, pKa, pK_ion)
    in_arcsinh = 134 * electron_charge * x_charged/ (20 * np.sqrt(c_ion + 10**(-pH))) #Assume A = 20
    return 2*kB*T/electron_charge * np.arcsinh(in_arcsinh)

def surface_ion_num(c_ion, pH, pKa, pK_ion):
    x_ion = get_x_ion(c_ion, pH, pKa, pK_ion)
    phi0 = potential(c_ion, pH, pKa, pK_ion)
    ion_z0 = c_ion * np.exp(electron_charge * phi0 / kB / T) #ion concentration at z = 0, need to convert to fraction
    x_z0 = avo_num / 1e27 * 20 * ion_z0
    return x_ion + x_z0

def surface_ion_num_list(conc_list, pH, pKa, pK_ion):
    surf_ion_list = []
    for c in conc_list:
        surf_ion = surface_ion_num(c, pH, pKa, pK_ion)
        surf_ion_list.append(surf_ion)
    return surf_ion_list


print(get_x_total(1e-2, pH, pKa))
print(get_x_ion(1e-2, pH, pKa, pK_ion = 0.6))

conc_list = np.logspace(-6, 1, 1000)
pK_ion_list = [-0.249, -0.057, 0.228, 0.318, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'SCN', 'I']
plt.figure()
for i in range(len(pK_ion_list)):
    x_ion = adsorb_frac(conc_list, pH, pKa, pK_ion_list[i])
    plt.semilogx(conc_list, x_ion, markersize = 1, label = label_list[i])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion adsorption fraction at neutral pH')
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/ion adsorption semilog')
plt.show()

plt.figure()
pK_ion_list = [-0.249, -0.057, 0.228, 0.318, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'SCN', 'I']
conc_list_small = np.linspace(1e-4, 1e-3, 100)
for j in range(len(pK_ion_list)):
    x_ion_small = adsorb_frac(conc_list_small, pH, pKa, pK_ion_list[j])
    plt.plot(conc_list_small, x_ion_small, markersize = 1, label = label_list[j])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion adsorption fraction at neutral pH')
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/ion adsorption small range')
plt.show()

conc_list = np.logspace(-6, 1, 1000)
pK_ion_list = [-0.249, -0.057, 0.228, 0.318, 0.515, 0.672]
label_list = ['F', 'Cl', 'Br', 'NO3', 'SCN', 'I']
plt.figure()
x_total = ionization_frac(conc_list, pH, pKa)
for i in range(len(pK_ion_list)):
    x_ion = adsorb_frac(conc_list, pH, pKa, pK_ion_list[i])
    x_charged = np.array(x_total)-np.array(x_ion)
    plt.semilogx(conc_list, x_charged, markersize = 1, label = label_list[i])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('fraction of charged ODA')
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/ODA charged fraction')
plt.show()



conc_list = np.linspace(1e-6, 1e-3, 1000)
plt.figure()
for i in range(len(pK_ion_list)):
    surf_ion = surface_ion_num_list(conc_list, pH, pKa, pK_ion_list[i])
    plt.plot(conc_list, surf_ion, markersize = 1, label = label_list[i])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion population at surface (bonded + free)')
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/surface ion population')
plt.show()


plt.figure()
conc_list_Br = np.linspace(1e-6, 1e-3, 100)
x_Br = adsorb_frac(conc_list_Br, pH, pKa, pK_ion=0.228)
print(x_Br)
x_proton_Br = ionization_frac(conc_list_Br, pH, pKa)
Br_num = surface_ion_num_list(conc_list_Br, pH, pKa, pK_ion = 0.228)
print(Br_num)
plt.plot(conc_list_Br, x_Br, markersize = 1, label = 'predicted adsorbed ion ratio')
plt.plot(conc_list_Br, x_proton_Br, markersize = 1, label = 'predicted ionization ratio')
plt.plot(conc_list_Br, Br_num, markersize = 1, label = 'predicted ion/head ratio')
conc_Br = 1e-3 * np.array([0.05, 0.1, 0.15, 0.2, 0.25,
                           0.3, 0.4, 0.5, 0.6, 0.75])
ion_cov = np.array([0.1056, 0.12958, 0.31523, 0.3315, 0.33966,
           0.36186, 0.3975, 0.41055, 0.5936, 0.63248])
plt.scatter(conc_Br, ion_cov, label = 'XRF fitted ion/head ratio')
plt.legend()
plt.savefig('/Users/rachel/NU research/graphs/Model vs XRF')
plt.show()





