import os

import matplotlib.pyplot as plt

main_folder = '/Users/rachel/Isotherms/'
os.chdir(main_folder)
folder1 = 'KF_ODA_2023_4'
from utils.plot_functions import plot_folder_shifted, plot_folder

plot_folder_shifted(folder1)
plt.savefig('shifted_isotherms.png')

'''
from utils.math_functions import find_area_at_pressure
from utils.input_output import sort_file
from utils.math_functions import find_kink
#filenames = os.listdir(os.path.join(main_folder, folder1))
filenames = sort_file(os.path.join(main_folder, folder1))
area_list = []
kink_list = []
for i in range(len(filenames)):
    print(filenames[i])
    area = find_area_at_pressure(7, filenames[i])
    kink_p = find_kink(filenames[i])
    area_list.append(area)
    kink_list.append(kink_p)
print(area_list)

conc_list = [0.01, 0.025, 0.05, 0.075, 0.1, 0.125]
kink_list = [3.75, 6.25, 8.25, 10.5, 12.5, 13]
plt.figure()
plt.scatter(conc_list, kink_list)
plt.xlabel('concentration(mM)')
plt.ylabel('transition pressure(dynes)')
plt.title('KSCN')
plt.savefig('KSCN_kink_pressure.png')
plt.show()
'''
conc_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.5]
from utils.plot_functions import plot_kink_fig
plot_kink_fig(folder1, conc_list)