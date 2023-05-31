import numpy as np
import os
import re


mw = 269.5
conc = 0.278 #concentration in mg/ml
add_volume = 100 #in ul
avogadros_num = 6.02e23
num_molecules = conc * add_volume/1e3 * avogadros_num/mw
def get_data_lab(filename): #get XF data from fluo_data
    troughlength = 205
    troughwidth = 120
    barrier_position = []
    pressure = []
    f = open(filename, 'r')
    line = f.readline()
    while(line[0].isnumeric() != True):
        line = f.readline()
    while(line and line != '}\n'):
        if '\\tab' in line:
            # Split using '\tab'
            data = re.split(r'\s*\\tab\s*', line)
        else:
            # Split using '\t'
            data = line.split()
        barrier_position.append(float(data[1]))
        pressure.append(float(data[5])) # I = 2D array of energies = energies each Qz
        line = f.readline()
    f.close()
    area = [(troughlength - x) * troughwidth for x in barrier_position]
    area_per_m = [x/num_molecules * 1e17 for x in area]
    return area_per_m, pressure


# def get_data_5clmn(filename):
#     area = []
#     pressure = []
#     f = open(filename, 'r')
#     line = f.readline()
#     while line:
#         data = line.split()
#         if data[1].isdigit():
#             area.append((43344-float(data[1])) * 1e14 / num_molecules)
#             pressure.append(float(data[4]))
#         line = f.readline()
#     f.close()
#     return area, pressure


#sort the files in folder in order of the number in the filename, and return the sorted filenames as a list
def sort_file(foldername):
    filenames = os.listdir(foldername)
    num = []
    for name in filenames:
        if name[-3:] != 'txt' and name[-3:] != 'rtf':
            continue
        else:
            name_number = re.findall('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', name)
            if len(name_number) == 0:
                n = 0
            else:
                n = sum(float(x) for x in name_number)
            num.append([n, name])
    num.sort(key = lambda x:x[0])
    return [x[1] for x in num]

def shift_data_lab(filename):
    area, pressure = get_data_lab(filename)
    from utils.math_functions import find_collapse_area
    from utils.math_functions import fit_piecewise
    p0, p1, p2, a0, a1, a2 = fit_piecewise(filename)
    area_shift = 19 - a2
    area_shifted = np.array(area) + area_shift
    area_shifted.tolist()
    pressure_shifted = np.array(pressure) - p0
    pressure_shifted.tolist()
    # Save data to text file
    import os

    # Define the new folder path
    folder_path = './calibrated_data'

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the new folder if it doesn't exist
        os.makedirs(folder_path)
    save_path = os.path.join(folder_path, filename)
    with open(save_path, 'w') as f:
        f.write('area_shifted\tpressure\n')
        for i in range(len(area)):
            f.write('{}\t{}\n'.format(area_shifted[i], pressure_shifted[i]))
        f.close()
    return area_shifted, pressure_shifted

'''
def get_data_APS(filename):
'''
