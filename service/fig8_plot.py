import matplotlib.pyplot as plt
import numpy as np
import os

concentrations = [0.1, 0.5, 1, 5]
ion_head_ratio = [0.378, 0.176, 0.330]

fig, ax = plt.subplots()
ax.bar(ions, ion_head_ratio, width = 0.4)
ax.set_ylabel('ion/head ratio')
fig.savefig('/Users/rachel/NU research/paper_fig7.png')
fig.show()