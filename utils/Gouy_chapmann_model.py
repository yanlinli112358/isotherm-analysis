import numpy as np
import matplotlib.pyplot as plt
##Reference: https://pubs.acs.org/doi/10.1021/jp809443d
A = 20 #area of ionization site in Angstroms. 20 for ODA (or most signle chain surf)
electron_charge = 1.602e-19
kB = 1.38e-23
T = 273.5 + 20
epsilon0 = 8.85e-12
epsilonr = 78.5

def ion_frac(salt_conc, pH, pKa, A):
    #returns ionization fraction of the monolayer at a given pH and  salt bulk concentration
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
    return electron_charge * x / A

def surface_potential(conc, pH, pKa, A):
    x = ion_frac(conc, pH, pKa, A)
    return 2*kB*T / electron_charge * np.arcsinh(134 * x / A / np.sqrt(conc + 10**(-pH)))

##Davis function
##Source: https://pubs.acs.org/doi/10.1021/jp809443d
def delta_pi(conc, pH, pKa, A):
    sigma = surface_charge_den(conc, pH, pKa, A)
    x = ion_frac(conc, pH, pKa, A)
    phi = surface_potential(conc, pH, pKa, A)
    tanh = np.tanh(electron_charge * phi / (4 * kB * T))
    dPi = 2 * kB * T * x / (A * 1e-20) * tanh / electron_charge
    return dPi

def ion_profile(z, conc, pH, pKa, A):
    #returns the surface ion profile as a function of z -- distance from surface
    #use poisson distribution
    potential_0 = surface_potential(conc, pH, pKa, A)
    print(potential_0)
    kapa_squared = 2 * electron_charge**2 * (conc + 10**(-pH)) / (epsilonr * epsilon0 * kB * T) #kapa = 1/debye length
    print(np.sqrt(kapa_squared))
    potential = np.exp(-np.sqrt(kapa_squared) * z)
    print(potential)
    return conc * np.exp(-electron_charge * potential) / kB / T

