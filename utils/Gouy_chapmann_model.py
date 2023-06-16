import numpy as np
##Reference: https://pubs.acs.org/doi/10.1021/jp809443d
A = 20 #area of ionization site in Angstroms. 20 for ODA (or most signle chain surf)
electron_cahrge = 1.602e-19
kB = 1.38e-23
T = 273.5 + 20
epsilon0 = 8.85e-12
epsilonr = 78.5

def ion_frac(salt_conc, pH, pKa, A):
    #g = LHS of eq(4) in 'Salt promotes protonation'
    def g(salt_conc, pH):
        return np.sqrt(salt_conc + 10 ** (-pH))
    #f = RHS of eq(4)
    def f(pH, pKa, x):
        temp = (np.log10((1 - x) / x) - pH + pKa) / 0.87
        return 134 * x /(A * np.sinh(temp))
    #objective = abs(LHS-RHS)
    def objective(x):
        return abs(g(salt_conc, pH) - f(pH, pKa, x))
    #res is the solutions that minimize the difference b/w LHS and RHS
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')

    return res.x

def surface_charge_den(conc, pH, pKa, A):
    x = ion_frac(conc, pH, pKa, A)
    return electron_cahrge * x / A

def surface_potential(conc, pH, pKa, A):
    x = ion_frac(conc, pH, pKa, A)
    #factor = electron_cahrge / np.sqrt(8 * epsilonr * epsilon0 * kB * T)
    return 2*kB*T / electron_cahrge * np.arcsinh(134 * x / A / np.sqrt(conc))

##Davis function
##Source: https://pubs.acs.org/doi/10.1021/jp809443d
def delta_pi(conc, pH, pKa, A):
    sigma = surface_charge_den(conc, pH, pKa, A)
    x = ion_frac(conc, pH, pKa, A)
    phi = surface_potential(conc, pH, pKa, A)
    tanh = np.tanh(electron_cahrge * phi / (4 * kB * T))
    print(tanh)
    dPi = 2 * kB * T * x / (A * 1e-20) * tanh / electron_cahrge
    return dPi

conc = 1e-3
print(ion_frac(conc, 5.7, 10.5, A))
print(surface_potential(conc, 5.7, 10.5, A))
print(delta_pi(conc, 5.7, 10.5, A))

