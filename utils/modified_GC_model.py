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
    #gives the total fraction of all ionized amines
    #g = LHS of eq(4) in 'Salt promotes protonation'
    def g(c_ion, pH):
        return np.sqrt(c_ion + 10 ** (-pH))
    #f = RHS of eq(4)
    def f(pH, pKa, x):
        temp = (np.log10((1 - x) / x) - pH + pKa) / 0.87
        return 134 * x / (25 * np.sinh(temp)) ## ODA area = 20
    #objective = abs(LHS-RHS)
    def objective(x):
        return abs(g(c_ion, pH) - f(pH, pKa, x))
    #res is the solutions that minimize the difference b/w LHS and RHS
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')

    return res.x

def get_x_ion(c_ion, pH, pKa, pK_ion):
    #give the fraction of ionized amines that adsorbs an ion
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
    # def g(pH, pKa, pK_ion):
    #     return pH - pKa - pK_ion
    # def f(x_ion, c_ion, pH, pKa):
    #     x = x_total
    #     return np.log10((1-x) / x) + np.log10((x - x_ion) / x_ion) + np.log10(c_ion)
    # def objective(x_ion):
    #     return abs(g(pH, pKa, pK_ion) - f(x_ion, c_ion, pH, pKa))
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, x_total), method='bounded')
    return res.x

def get_x_proton(c_ion, pH, pKa, pK_ion):
    #gives the fraction of ionized amines that does not adsorb an ion
    x_total = get_x_total(c_ion, pH, pKa)
    x_ion = get_x_ion(c_ion, pH, pKa, pK_ion)
    return x_total - x_ion

def ionization_frac(conc_list, pH, pKa):
    #given a list of salyt concentrations and given bulk pH and pKa of amine
    #produces a list of ionization fraction as a function of salt concentration
    ion_frac = []
    for c in conc_list:
        x = get_x_total(c, pH, pKa)
        ion_frac.append(x)
    return ion_frac

def adsorb_frac(conc_list, pH, pKa, pK_ion):
    #given a list of concentrations and given bulk pH and pKa of amine
    #produces a list of adsorbed ion fraction as a function of concentration
    ion_frac = []
    for c in conc_list:
        x = get_x_ion(c, pH, pKa, pK_ion)
        ion_frac.append(x)
    return ion_frac

def potential(c_ion, pH, pKa, pK_ion):
    #gives the surface potential at a given salt concentration and pH
    x_charged = get_x_proton(c_ion, pH, pKa, pK_ion)
    in_arcsinh = 134 * electron_charge * x_charged/ (20 * np.sqrt(c_ion + 10**(-pH))) #Assume A = 20
    return 2*kB*T/electron_charge * np.arcsinh(in_arcsinh)

def surface_ion_num(c_ion, pH, pKa, pK_ion):
    #gives the number (instead of fraction) of ions at surface at a given bulk concentration and pH
    x_ion = get_x_ion(c_ion, pH, pKa, pK_ion)
    phi0 = potential(c_ion, pH, pKa, pK_ion)
    ion_z0 = c_ion * np.exp(electron_charge * phi0 / kB / T) #ion concentration at z = 0, need to convert to fraction
    x_z0 = avo_num / 1e27 * 20 * ion_z0
    return x_ion + x_z0

def surface_ion_num_list(conc_list, pH, pKa, pK_ion):
    #give a list of ion population near surface as a function of concentration
    surf_ion_list = []
    for c in conc_list:
        surf_ion = surface_ion_num(c, pH, pKa, pK_ion)
        surf_ion_list.append(surf_ion)
    return surf_ion_list


print(get_x_total(1e-2, pH, pKa))
print(get_x_ion(1e-2, pH, pKa, pK_ion = 0.6))

conc_list = np.logspace(-6, 1, 1000)
pK_ion_list = -np.log10(np.array([1.774, 1.142, 0.592, 0.48, 0.312, 0.305, 0.213]))
print(pK_ion_list)
label_list = ['F', 'Cl', 'Br', 'NO3', 'ClO4', 'SCN', 'I']

plt.figure()
for i in range(len(pK_ion_list)):
    x_ion = adsorb_frac(conc_list, pH, pKa, pK_ion_list[i])
    plt.semilogx(conc_list, x_ion, markersize = 1, label = label_list[i])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion adsorption fraction at pH 5.7')
    plt.legend()
plt.savefig('/Users/rachel/NU research/graphs/ion adsorption semilog')
plt.show()

plt.figure()
conc_list_small = np.linspace(1e-4, 1e-3, 100)
for j in range(len(pK_ion_list)):
    x_ion_small = adsorb_frac(conc_list_small, pH, pKa, pK_ion_list[j])
    plt.plot(conc_list_small, x_ion_small, markersize = 1, label = label_list[j])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion adsorption fraction at pH 5.7')
    plt.ylim(0, 1)
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/ion adsorption small range')
plt.show()

plt.figure()
conc_list_small = np.linspace(1e-4, 1e-3, 100)
for j in range(len(pK_ion_list)):
    x_ion_small = adsorb_frac(conc_list_small, 4, pKa, pK_ion_list[j])
    plt.plot(conc_list_small, x_ion_small, markersize = 1, label = label_list[j])
    plt.xlabel('salt concentration(M)')
    plt.ylabel('ion adsorption fraction at pH 4')
    plt.ylim(0, 1)
    plt.legend()

plt.savefig('/Users/rachel/NU research/graphs/ion adsorption pH4')
plt.show()


plt.figure()
conc_list = np.linspace(1e-6, 1e-3, 100)
x_I = adsorb_frac(conc_list, pH, pKa, pK_ion=pK_ion_list[-1])
x_Cl = adsorb_frac(conc_list, pH, pKa, pK_ion=pK_ion_list[2])
x_ClO4 = adsorb_frac(conc_list, pH, pKa, pK_ion=pK_ion_list[-3])
x_Br = adsorb_frac(conc_list, pH, pKa, pK_ion=pK_ion_list[3])
print(x_I)
plt.plot(conc_list, x_I, markersize = 1, label = 'predicted adsorbed I ratio')
plt.plot(conc_list, x_Cl, markersize = 1, label = 'predicted adsorbed Cl ratio')
plt.plot(conc_list, x_ClO4, markersize = 1, label = 'predicted adsorbed ClO4 ratio')
#plt.plot(conc_list, x_Br, markersize = 1, label = 'predixted adsorbed Br ratio')
#x_proton_I = ionization_frac(conc_list_I, pH, pKa)
#plt.plot(conc_list_I, x_proton_I, markersize = 1, label = 'predicted ionization ratio')
c_data_I = 1e-3* np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
y_data_I = np.array([0.071, 0.150, 0.203, 0.328, 0.362, 0.378, 0.421, 0.410])
c_data_Cl = 1e-3*np.array([0.4, 0.5])
y_data_Cl = [0.152, 0.176]
y_data_ClO4 = [0.251, 0.330]

plt.scatter(c_data_I, y_data_I, label = 'XF data I')
plt.scatter(c_data_Cl, y_data_Cl, label='XF data Cl')
plt.scatter(c_data_Cl, y_data_ClO4, label='XF data ClO4')
plt.legend()
plt.xlabel('ion concentration (M)')
plt.ylabel('ion-amine ratio')
plt.savefig('/Users/rachel/NU research/graphs/Model vs XRF')
plt.show()





