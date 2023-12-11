ion_dic = {
    'F':{
        'conc_list': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.25, 1.5, 2, 3, 4, 5, 7, 10, 15],
        'folder': 'KF_ODA_2023_4'
    },

    'NO3': {
        'conc_list': [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75],
        'folder': 'KNO3_ODA_2023_6'
    },

    'Cl':{
        'conc_list': [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 0.817, 1.10, 1.5, 2.15, 2.69, 3, 5],
        'folder': 'KCl_ODA_2023_1'
    },

    'Br': {
        'conc_list': [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1, 1.5, 2],
        'folder': 'KBr_ODA_2023_1'
    },

    'I': {
        'conc_list': [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 0.75, 1, 1.25],
        'folder': '/Users/rachel/Isotherms/KI_ODA_2023_1'
    },

    'SCN': {
        'conc_list': [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1],
        'folder': 'KSCN_ODA_2023_6'
    },

    'SO4': {
        'conc_list': [0, 0.0025, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.05, 0.075, 0.1]
    },

    'ClO4': {
        'conc_list': [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6],
        'folder': 'KClO4_ODA_2023_6'
    },

    'BF4': {
        #'conc_list': [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75],
        'conc_list': [0, 0.01, 0.015, 0.02, 0.025, 0.035, 0.05, 0.06, 0.075, 0.1],
        'folder': 'KBF4_ODA_2023_8',
    },

    'ClO4_2': {
        'conc_list': [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4],
        'folder': 'KClO4_ODA_2023_7'
    },

    'ClO4_3':{
        'conc_list': [0, 0.025, 0.035, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4],
        'folder': 'KClO4_ODA_second_2023_7'
    }
}


avogadros_num = 6.02e23
molecule_dic = {}
def add_molecule(name, mw, conc, add_volume):
    #mw = molecular weight in g/mol
    #conc = concentration of molecule in solvent in mg/ml
    #add_volume = volume spreaded on surface in ul
    avogadros_num = 6.02e23
    num_molecules = conc * add_volume/1e3 * avogadros_num/mw
    molecule_dic[name] = {'mw': mw, 'conc': conc, 'add_volume': add_volume,
                      'num_molecules': num_molecules}

add_molecule('ODA', 269.5, 3.2, 60)
print(molecule_dic)


