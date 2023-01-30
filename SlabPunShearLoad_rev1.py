import pandas as pd
from GetAxialForceDiff_rev4 import GetAxialForceDiff
from functools import reduce


'''Gets column forces and frame assignment tables and outputs dataframe with punching shear load (Axial_Diff)
for each level. 
note: Concrete Frame Design must be run. script reads the design section, not analysis section.
note: for a model with just one story/level punching shear load = axial force in column
note: if copying this code to console, don't forget to make console directory same as excel tables location
and reload python console
'''

### INPUTS SECTION ###

# type exported story data etabs table below
# Model  > Structure Layout > Story Data
story_data_excel = 'Etabs - story data.xlsx'

# type exported frame assignments etabs table below
# etabs table to be exported: Model > Assignments > Frame Assignments > Frame Assignments - Summary
frame_assignments_excel = 'Etabs - frame assignments.xlsx'

# type exported column forces etabs table below
# Analysis > Results > Frame Results > Column Forces
column_forces_excel = 'Etabs - column forces.xlsx'

load_case = 'ULS-grav'  # select load case for punching shear


### END OF INPUTS SECTION ###
### ----------------- ###

# import tables from excel to python (change console directory in File>Settings>Console>Python Console>Working Directory)
#to the same directory where the tables are saved
column_forces = pd.read_excel(column_forces_excel, header=1)
column_forces = column_forces.drop(0)  # drop units row
frame_assignments = pd.read_excel(frame_assignments_excel, header=1)
frame_assignments = frame_assignments.drop(0)  # drop units row
story_data = pd.read_excel(story_data_excel, header=1)
story_data = story_data.drop(0) # drop units row

# select all stories except base
story_data = story_data.sort_values(by='Elevation')
story_data = story_data.iloc[1:, :]  # drop base story
stories = story_data['Name']
stories = list(stories)  # convert stories into list to iterate


# filter by ULS case only
column_forces = column_forces[column_forces['Load Case/Combo'] == load_case]

dfs = []  # initialize empty list to store axial forces difference dataframe for each floor

# if more than one story, merge axial column loads from pillars above the slab in consideration...
#...with pillars below the slab to get the difference between axial load
if len(stories) > 1:

    for i in range(len(stories)-1):
        upper_floor = stories[i+1]
        lower_floor = stories[i]

        # merge lower floor and upper floor data and store it in a list
        dfs.append(GetAxialForceDiff(column_forces, frame_assignments, load_case, upper_floor, lower_floor))

    # merge dataframes stored in the list
    dfs_merged = reduce(lambda left, right: pd.merge(left, right,on=['Column'],
                                                how='outer'), dfs)

### add upper story data ###

# get upper station of upper floor column
upper_column_forces = column_forces[column_forces['Story'] == stories[-1]]
max_station = max(upper_column_forces['Station'])
upper_column_forces = upper_column_forces[upper_column_forces['Station'] == max_station]

# add design section column
upper_column_forces = upper_column_forces.merge(frame_assignments[["Unique Name", "Design Section"]], how="left", on="Unique Name")

# filter features of interest
upper_column_forces = upper_column_forces[['Column', 'Design Section', 'P']]

if len(stories) > 1: # if more than one story, merge data from upper floor pillars with stories below

# merge upper_column data with lower stories data
    dfs_merged = dfs_merged.merge(upper_column_forces[["Column", "Design Section", "P"]], how="outer", on="Column")

    # rename columns to improve readability
    dfs_merged.rename(columns={'Design Section': 'Design Section - ' + stories[-1],
                                       'P': 'P - ' + stories[-1],
                                    }, inplace=True)

    # export dataframe to excel
    dfs_merged.to_excel('PunchingShearLoads - ' + column_forces_excel)


# export dataframe to excel (if just one floor model)
if len(stories) == 1:
    upper_column_forces.to_excel('PunchingShearLoads - ' + column_forces_excel)




