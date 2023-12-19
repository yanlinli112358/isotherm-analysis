import numpy as np
import os
import re


mw = 269.5
conc = 0.278 #concentration in mg/ml
add_volume = 60 #in ul
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

def write_area_pressure(savename, area, pressure):
    with open(savename, 'w') as f:
        f.write('area\tpressure\n')
        for i in range(len(area)):
            f.write('{}\t{}\n'.format(area[i], pressure[i]))
        f.close()
    return None

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
    new_list = [x[1] for x in num]

    return new_list

def shift_data_lab(filename):
    area, pressure = get_data_lab(filename)
    from utils.math_functions import find_kink_df
    p_kink = find_kink_df(filename)
    kink_index = pressure.index(p_kink)
    area_shift = 20 - area[kink_index]
    area_shifted = np.array(area) + area_shift
    area_shifted.tolist()
    # # Define the new folder path
    # folder_path = './calibrated_data'
    # # Check if the folder already exists
    # if not os.path.exists(folder_path):
    #     # Create the new folder if it doesn't exist
    #     os.makedirs(folder_path)
    # save_path = os.path.join(folder_path, 'shifted_' + filename)

    savename = filename[:-4] + '_shfited' + filename[-4:]
    #write_area_pressure(savename, area_shifted, pressure)
    return area_shifted, pressure

'''
def get_data_APS(filename):
'''
def read_monolayer(filename):
    import csv
    # Create an empty dictionary to store the data
    monolayer_dict = {}
    # Read the CSV file and populate the dictionary
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            subphase = row['subphase']
            mw = float(row['mw'])
            stock_conc = float(row['stock_conc'])
            add_volume = float(row['add_volume'])

            monolayer_dict[subphase] = {
                'mw': mw,
                'stock_conc': stock_conc,
                'add_volume': add_volume
            }
    return monolayer_dict

def calibrate_folder_different_monolayer(foldername):
    filenames = sort_file(foldername)
    if os.listdir(foldername).__contains__('monolayer_info.csv'):
        monolayer_dict = read_monolayer(os.path.join(foldername, 'monolayer_info.csv'))
        for file in filenames:
            ## read the barrier position and pressure first
            barrier_position = []
            pressure = []
            filepath = os.path.join(foldername, file)
            f = open(filepath, 'r')
            line = f.readline()
            while (line[0].isnumeric() != True):
                line = f.readline()
            while (line and line != '}\n'):
                if '\\tab' in line:
                    # Split using '\tab'
                    data = re.split(r'\s*\\tab\s*', line)
                else:
                    # Split using '\t'
                    data = line.split()
                barrier_position.append(float(data[1]))
                pressure.append(float(data[5]))  # I = 2D array of energies = energies each Qz
                line = f.readline()
            f.close()

            ## calibrate the area per molecule according to recorded monolayer info
            subphase = file[:-4]
            troughlength = 205
            troughwidth = 120
            if subphase in monolayer_dict:
                print(subphase)
                mw = monolayer_dict[subphase]['mw']
                stock_conc = monolayer_dict[subphase]['stock_conc']
                add_volume = monolayer_dict[subphase]['add_volume']
                num_molecules = stock_conc * add_volume / 1e3 * avogadros_num / mw
                area = [(troughlength - x) * troughwidth for x in barrier_position]
                area_per_m = [x / num_molecules * 1e17 for x in area]
                #save the calibrated data into calibrated folder
                savepath = os.path.join(foldername, 'calibrated_data')
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                savename = subphase + '.txt'
                f_save = open(os.path.join(savepath, savename), 'w')
                data_combined = list(zip(area_per_m, pressure))
                for x, y in data_combined:
                    f_save.write(f"{x} {y}\n")
                f_save.close()
    else:
        print('The folder has same monolayer for each file. use get_data_lab instead')


