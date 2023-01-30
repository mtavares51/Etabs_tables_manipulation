import pandas as pd
import numpy as np


from find_nearest import find_nearest
from MaxBeamForces_rev1 import max_beam_forces


def get_beam_forces(beamforces_dataframe, unique_name, stations):
    '''Prints internal forces for the nearest etabs station given by station parameter'''
    '''beamforces_dataframe - etabs exported table "Beam Forces"'''
    '''unique_name - beam we want to retrieve internal forces'''
    '''stations - locations (x coordinate) we want to retrieve internal forces'''

    # filter required beam by unique name
    beamforces_dataframe = beamforces_dataframe[beamforces_dataframe["Unique Name"] == unique_name]

    # initialize vectors to store data
    e_stations = ['']*len(stations)
    M_uls = ['']*len(stations)
    V = ['']*len(stations)
    M_sls = ['']*len(stations)
    T = ['']*len(stations)


    for i in range(len(stations)):

        e_stations[i] = find_nearest(beamforces_dataframe["Station"], stations[i])

        # filter by required station
        beamforces_dataframe1 = beamforces_dataframe[beamforces_dataframe["Station"] == e_stations[i]]
        # get internal forces
        M_uls[i] = beamforces_dataframe1[beamforces_dataframe1["Load Case/Combo"] == 'ULS-grav'].sort_values('abs(M3)', ascending = False).iloc[0,:]['M3']
        V[i] = beamforces_dataframe1[beamforces_dataframe1["Load Case/Combo"] == 'ULS-grav'].sort_values('abs(V2)', ascending = False).iloc[0, :]['abs(V2)']
        M_sls[i] = beamforces_dataframe1[beamforces_dataframe1["Load Case/Combo"] == 'SLS'].sort_values('abs(M3)', ascending = False).iloc[0,:]['M3']
        T[i] = beamforces_dataframe1[beamforces_dataframe1["Load Case/Combo"] == 'ULS-grav'].sort_values('abs(T)', ascending = False).iloc[0,:]['abs(T)']

    label = beamforces_dataframe.iloc[0, :]["Beam"]
    story = beamforces_dataframe.iloc[0, :]["Story"]
    un_nm = str(unique_name)
    h = beamforces_dataframe.iloc[0, :]["t3"]
    b = beamforces_dataframe.iloc[0, :]["t2"]

    e_stations = np.array(e_stations)
    e_stations = np.round(e_stations, 2)

    forces_dic = {'Unique Name': un_nm,
                  'Label': label,
                  'Story': story,
                  'h': h,
                  'b': b,
                  'Station': e_stations,
                  'M_uls': M_uls,
                  'V': V,
                  'M_sls': M_sls,
                  'T': T,
                  }

    forces_df = pd.DataFrame(forces_dic)


    max_forces_df = max_beam_forces(beamforces_dataframe, unique_name)

    forces_df = pd.concat([forces_df, max_forces_df]).reset_index(drop=True)

    #forces_df.to_excel("BeamForces_" + str(label) + "_" + un_nm + ".xlsx")

    #print(forces_df)

    print(label + '_' + un_nm + ' @ ' + story)

    return forces_df
