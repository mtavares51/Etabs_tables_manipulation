import pandas as pd


def max_beam_forces(beamforces_dataframe, unique_name):

    '''Prints maximum internal forces for an RC section'''
    '''beamforces_dataframe - etabs exported table "Beam Forces"'''
    '''unique_name - beam we want to retrieve internal forces (unique name in etabs)'''

    e_stations = []
    M_uls = []
    V = []
    M_sls = []
    T = []

    # filter required beam by unique name
    beamforces_dataframe = beamforces_dataframe[beamforces_dataframe["Unique Name"] == unique_name]

    # filter uls & sls combos
    beamforces_dataframe_uls = beamforces_dataframe[beamforces_dataframe["Load Case/Combo"] == 'ULS-grav']
    beamforces_dataframe_sls = beamforces_dataframe[beamforces_dataframe["Load Case/Combo"] == 'SLS']

    # get maximum hogging moment and corresponding shear and torsion
    max_hogging_M_uls_df = beamforces_dataframe_uls.sort_values('M3', ascending=True)
    max_hogging_M_uls_station = max_hogging_M_uls_df.iloc[0, :]['Station']
    max_hogging_M_uls_df = max_hogging_M_uls_df[max_hogging_M_uls_df['Station'] == max_hogging_M_uls_station]
    max_hogging_M_uls = max_hogging_M_uls_df.iloc[0, :]['M3']
    max_hogging_V = max_hogging_M_uls_df.sort_values('abs(V2)', ascending=False).iloc[0, :]['abs(V2)']
    max_hogging_T = max_hogging_M_uls_df.sort_values('abs(T)', ascending=False).iloc[0, :]['abs(T)']

    max_hogging_M_sls_df = beamforces_dataframe_sls[beamforces_dataframe_sls["Station"] == max_hogging_M_uls_station]
    max_hogging_M_sls = max_hogging_M_sls_df.sort_values('abs(M3)', ascending=True).iloc[0, :]['M3']

    e_stations.append(max_hogging_M_uls_station)
    M_uls.append(max_hogging_M_uls)
    V.append(max_hogging_V)
    M_sls.append(max_hogging_M_sls)
    T.append(max_hogging_T)

    # get maximum sagging moment and corresponding shear and torsion
    max_sagging_M_uls_df = beamforces_dataframe_uls.sort_values('M3', ascending=False)
    max_sagging_M_uls_station = max_sagging_M_uls_df.iloc[0, :]['Station']
    max_sagging_M_uls_df = max_sagging_M_uls_df[max_sagging_M_uls_df['Station'] == max_sagging_M_uls_station]
    max_sagging_M_uls = max_sagging_M_uls_df.iloc[0, :]['M3']
    max_sagging_V = max_sagging_M_uls_df.sort_values('abs(V2)', ascending=False).iloc[0, :]['abs(V2)']
    max_sagging_T = max_sagging_M_uls_df.sort_values('abs(T)', ascending=False).iloc[0, :]['abs(T)']

    max_sagging_M_sls_df = beamforces_dataframe_sls[beamforces_dataframe_sls["Station"] == max_sagging_M_uls_station]
    max_sagging_M_sls = max_sagging_M_sls_df.sort_values('abs(M3)', ascending=False).iloc[0, :]['M3']

    e_stations.append(max_sagging_M_uls_station)
    M_uls.append(max_sagging_M_uls)
    V.append(max_sagging_V)
    M_sls.append(max_sagging_M_sls)
    T.append(max_sagging_T)

    # get maximum shear V2 in section and corresponding M3 values and torsion
    max_V_df = beamforces_dataframe_uls.sort_values('abs(V2)', ascending=False)
    max_V_station = max_V_df.iloc[0, :]['Station']
    max_V_df = max_V_df[max_V_df['Station'] == max_V_station]
    max_V = max_V_df.sort_values('abs(V2)', ascending=False).iloc[0, :]['abs(V2)']
    max_V_M_uls = max_V_df.sort_values('abs(M3)', ascending=False).iloc[0, :]['M3']
    max_V_T = max_V_df.sort_values('abs(T)', ascending=False).iloc[0, :]['abs(T)']

    max_V_sls_df = beamforces_dataframe_sls[beamforces_dataframe_sls["Station"] == max_V_station]
    max_V_M_sls = max_V_sls_df.sort_values('abs(M3)', ascending=False).iloc[0, :]['M3']

    e_stations.append(max_V_station)
    M_uls.append(max_V_M_uls)
    V.append(max_V)
    M_sls.append(max_V_M_sls)
    T.append(max_V_T)

    # get maximum torsion and corresponding shear and moment values
    max_T_df = beamforces_dataframe_uls.sort_values('abs(T)', ascending=False)
    max_T_station = max_T_df.iloc[0, :]['Station']
    max_T_df = max_T_df[max_T_df['Station'] == max_T_station]
    max_T = max_T_df.sort_values('abs(T)', ascending=False).iloc[0, :]['abs(T)']
    max_T_M_uls = max_T_df.sort_values('abs(M3)', ascending=False).iloc[0, :]['M3']
    max_T_V = max_T_df.sort_values('abs(V2)', ascending=False).iloc[0, :]['abs(V2)']

    max_T_sls_df = beamforces_dataframe_sls[beamforces_dataframe_sls["Station"] == max_T_station]
    max_T_M_sls = max_T_sls_df.sort_values('abs(M3)', ascending=False).iloc[0, :]['M3']

    e_stations.append(max_T_station)
    M_uls.append(max_T_M_uls)
    V.append(max_T_V)
    M_sls.append(max_T_M_sls)
    T.append(max_T)

    label = beamforces_dataframe.iloc[0, :]["Beam"]
    story = beamforces_dataframe.iloc[0, :]["Story"]
    un_nm = str(unique_name)
    h = beamforces_dataframe.iloc[0, :]["t3"]
    b = beamforces_dataframe.iloc[0, :]["t2"]

    max_forces_dic = {'Unique Name': un_nm,
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

    max_forces_df = pd.DataFrame(max_forces_dic)

    return max_forces_df