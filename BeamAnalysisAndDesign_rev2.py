import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from RCBeamMVDesign import rc_beam_M_V_design
from RCBeamTDesign import rc_beam_torsion_design
from BeamForces_rev7 import get_beam_forces
from ImportExcelTables import import_excel_tables


# etabs table to be exported: Model > Assignments > Frame Assignments > Frame Assignments - Summary
# input excel filename below
frame_assignments_excel = '211214 Building 1 REV42 - Frame Assignments.xlsx'

# etabs table to be exported: Analysis > Results > Frame Results > Beam Forces
# input excel filename below
beam_forces_excel = "211214 Building 1 REV42 - Beam Forces.xlsx"

# etabs table to be exported: Model>Definitions>Frame Sections>Frame Sections
# input excel filename below
frame_sections_excel = "211214 Building 1 REV42 - Frame Sections.xlsx"

# concrete grade of RC beams we want to design
concrete_grade = 'C30/37'

# imports etabs tables that were exported to excel
beam_forces, frame_count_df, frame_assignments = import_excel_tables(frame_assignments_excel,
                                                                       beam_forces_excel,
                                                                       frame_sections_excel,
                                                                       concrete_grade)

# define beam and stations we want to analyse and design
beam_unique_name = 936  # beam unique name we want to retrieve internal forces

# get beam length and array containing stations spaced 0.5
beam_length = frame_assignments[frame_assignments["Unique Name"] == beam_unique_name]["Length"].iloc[0] / 1000  # in meters
all_stations = np.arange(0, beam_length, 0.5)

# get beams forces for all stations and for maximum forces stations.
beam_forces_df_all = get_beam_forces(beam_forces, beam_unique_name, all_stations)
beam_forces_df_all = beam_forces_df_all.sort_values(by="Station")

# Uncomment below to plot M_uls
#beam_forces_df_all.plot(x = 'Station', y = 'M_uls', kind='line')
#plt.gca().invert_yaxis()
#plt.show(block=True)
#plt.interactive(False)

# stations we want to analyse and design (in meters) - ensure station < length of beam
stations = [1.09, 4.2, 8.2, 13.2, 17.2, 20.7, 24.2, 28.2, 32.2]
# get beams forces for stations above and for maximum forces stations
beam_forces_df = get_beam_forces(beam_forces, beam_unique_name, stations)

# create list of top rebar - ensure number of lines is equal to number of stations in beam_forces_df
bottom_rebar = [[[11, 20], ],
                [[11, 32], ],
                [[11, 20], ],
                [[11, 25], ],
                [[11, 20], ],
                [[11, 20], ],
                [[11, 20], ],
                [[11, 25], ],
                [[11, 20], ],
                [[11, 32], ],
                [[11, 32], ],
                [[11, 20], ],
                [[11, 20], ],
            ]

# create list of bottom rebar - ensure number of lines is equal to number of stations in beam_forces_df
top_rebar =    [[[11, 32], ],
                [[11, 20], ],
                [[11, 32], [11, 32]],
                [[11, 20], ],
                [[11, 32], [2, 32]],
                [[11, 20], ],
                [[11, 32], ],
                [[11, 20], ],
                [[11, 32], ],
                [[11, 32],  [11, 32]],
                [[11, 20], ],
                [[11, 32], [11, 32]],
                [[11, 32], ],

            ]
# create list of shear rebar - ensure number of lines is equal to number of stations in beam_forces_df
shear_rebar = [[7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               [7, 12, 200],
               ]

wk = 0.3 # set concrete crack width in mm
fck = 30 # set concrete resistance in MPa
c_nom_top = 35 # set concrete cover in mm, top zone
c_nom_bot = 35 # set concrete cover in mm, bottom zone
c_nom_s = 35 # set concrete cover in mm, sides

# run section design for each station in beam_forces_df
ratios, s_bar_top, s_bar_bottom = rc_beam_M_V_design(beam_forces_df, bottom_rebar, top_rebar, shear_rebar, c_nom_top, c_nom_bot, c_nom_s, wk, fck)

# unzip ratios vector to get Med and Ved ratios
ratios_unzipped = list(zip(*ratios))

# add ratios to beam dataframe
beam_forces_df['M_ratio'] = ratios_unzipped[0]
beam_forces_df['V_ratio'] = ratios_unzipped[1]

# add rebar info - bottom
beam_forces_df['bottom_rebar'] = bottom_rebar
beam_forces_df['s_bar_bottom'] = s_bar_bottom

# add rebar info - top
beam_forces_df['top_rebar'] = top_rebar
beam_forces_df['s_bar_top'] = s_bar_top

# add rebar info - shear
beam_forces_df['shear_rebar'] = shear_rebar


add_areas_torsion = rc_beam_torsion_design(beam_forces_df, bottom_rebar, top_rebar, shear_rebar, c_nom_top, c_nom_bot, fck)

# unzip add_areas_torsion vector to get additional longitudinal rebar and transverse rebar
add_areas_torsion_unzipped = list(zip(*add_areas_torsion))

# add ratios to beam dataframe
beam_forces_df['add_torsion_Asl'] = add_areas_torsion_unzipped[0]
beam_forces_df['add_torsion_Asw'] = add_areas_torsion_unzipped[1]

units_dict = {'Unique Name': '',
              'Label': '',
              'Story': '',
              'h': 'mm',
              'b': 'mm',
              'Station': 'm',
              'M_uls': 'kN.m',
              'V': 'kN',
              'M_sls': 'kN',
              'T': 'kN.m',
              'M_ratio': '',
              'V_ratio': '',
              'bottom_rebar': '[[n, diam],...]',
              's_bar_bottom': 'mm',
              'top_rebar': '[[n, diam],...]',
              's_bar_top': 'mm',
              'shear_rebar': '[n, diam, spacing]',
              'add_torsion_Asl': 'mm2',
              'add_torsion_Asw': 'mm2/m',
             }

# build units dataframe
units_df = pd.DataFrame(units_dict, index=[0])

# concatenate units dataframe with beam_forces_df dataframe putting units in first row
beam_forces_df = pd.concat([units_df, beam_forces_df], axis=0)

beam_forces_df.to_excel("BeamDesignData_" + str(beam_forces_df.iloc[1, :]["Label"]) + "_" +
                        str(beam_forces_df.iloc[1, :]["Unique Name"]) + ".xlsx")




'''
# try function manually
Beam_140 = beam_forces[beam_forces["Unique Name"] == 140]
etabs_station = find_nearest(Beam_140["Station"], 1.5)
Beam_140 = Beam_140[Beam_140["Station"] == etabs_station]
Beam_140 = Beam_140[Beam_140["Load Case/Combo"] == 'ULS-grav'].sort_values('abs(M3)', ascending = False)
Beam_140_M3 = Beam_140.iloc[0,:]['M3']

# extract width and depth from section_name
section_name = "RC Beam 1400x550dp"
numbers = []
temp_num = ""
for c in section_name:

    if c.isdigit():
        temp_num = temp_num + c

    elif temp_num != "":
        numbers.append(temp_num)
        temp_num = ""
'''