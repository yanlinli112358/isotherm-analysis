import numpy as py
##Reference: https://pubs.acs.org/doi/10.1021/jp809443d
def ion_frac(salt_conc, pH, pKa):
    #g = LHS of eq(4) in 'Salt promotes protonation'
    def g(salt_conc, pH):
        return np.sqrt(salt_conc + 10 ** (-pH))
    #f = RHS of eq(4)
    def f(pH, pKa, x):
        temp = (np.log10((1 - x) / x) - pH + pKa) / 0.87
        return 134 * x / (20 * np.sinh(temp))
    #objective = abs(LHS-RHS)
    def objective(x):
        return abs(g(salt_conc, pH) - f(pH, pKa, x))
    #res is the solutions that minimize the difference b/w LHS and RHS
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(objective, bounds=(0, 1), method='bounded')

    return res.x

electron_cahrge = 1.602e-19
def surface_charge_den(x, A):
    return electron_cahrge * x / A

##Davis function
def delta_pi
