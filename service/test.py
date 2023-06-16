import matplotlib.pyplot as plt
import numpy as np

from utils.Gouy_chapmann_model import delta_pi
conc_list_Br = 10e-3 * np.array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.5, 2])
pi_list = []
for conc in conc_list_Br:
    dPi = delta_pi(conc, 5.7, 10.5, 20)
    pi_list.append(dPi)

print(pi_list)
from utils.plot_functions import plot_kink_fig
conc_list = np.linspace(0.01, 2, 100) * 1e-3
pi_list2 = []
for conc in conc_list:
    dPi = delta_pi(conc, 5.7, 10.5, 20)
    pi_list2.append(dPi)
plt.plot(conc_list, pi_list2)
plt.show()


