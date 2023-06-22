'''this file models the Gouy-Chapmann in terms of HX- (hydrogen + an
anion X-) binding to NH2 instead of X- binding to NH3

Parameters in the model:
pKacid: pKA of the acid HX
pKA: pKA of the molecule ODA
pKd: pK (log dissociation) of the group HX- to NH2
c_ion: bulk concentration of the ion X- in M
A: area per ODA head, assume to be 20 A^2 across the model, not defined as parameter
'''
import numpy as np
import matplotlib.pyplot as plt

pH = 5.7
pKacid = 3.17
pKd = 0.318
pKA = 10.5
c_ion = 1e-3

def x_ion_expression(x_H, c_ion, pH, pKacid, pKd, pKA):
    c_total = c_ion + 10 ** (-pH)
    print(c_total)
    in_sinh = (134 * x_H)/ (20 * np.sqrt(c_total)) #A = 20
    print(np.arcsinh(in_sinh))
    pK_terms = pKacid +pKd -pKA
    print(pK_terms)
    power = pK_terms + np.log10(x_H) + np.log10(c_ion) + 0.87 * np.arcsinh(in_sinh)
    print(power)
    return 10 ** (power)

print(x_ion_expression(0.9, 1e-3, pH, pKacid, pKd, pKA))

def get_x_H(c_ion, pH, pKacid, pKd, pKA):
    def g(x_H, c_ion, pH):
        c_total = c_ion + 10 ** (-pH)
        return 0.87 * np.arcsinh(134 * x_H / (20 * np.sqrt(c_total)))

    def f(x_H, c_ion, pH, pKacid, pKd, pKA):
        x_ion = x_ion_expression(x_H, c_ion, pH, pKacid, pKd, pKA)
        return np.log10((1- x_H - x_ion) / x_H) - pH - pKA

    def objective(x_H):
        return abs(g(x_H, c_ion, pH) - f(x_H, c_ion, pH, pKacid, pKd, pKA))

    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return res.x

print(x_ion_expression(get_x_H(1e-3, 5.7, -9, 0.22, 10.5), 1e-3, 5.7, -9, 0.22, 10.5))

