

def GetAxialForceDiff(column_forces, frame_assignments, load_case, upper_floor, lower_floor):
    '''
    Outputs a dataframe of axial load difference between each adjacent story to calculate punching shear
    column_forces: dataframe with pillar (column) forces (etabs table)
    frame_assignments: dataframe with frame assignments (etabs table)
    load_case: load case for punching shear (Ultimate Limit State (gravitational loads)
    upper_floor: floor above slab in consideration for punching shear
    lower_floor: slab we want to obtain punching shear load

    note: Concrete Frame Design must be run. script reads the design section, not analysis section.
    WARNING: doesn't work for just one floor

    '''

    # filter bottom station of upper floor column
    column_forces_upper = column_forces[column_forces['Story']== upper_floor]
    min_station = min(column_forces_upper['Station'])
    column_forces_upper = column_forces[(column_forces['Story']== upper_floor) & (column_forces['Station']==min_station)]

    # filter top station of lower floor column
    column_forces_lower = column_forces[column_forces['Story']== lower_floor]
    max_station = max(column_forces_lower['Station'])
    column_forces_lower = column_forces[(column_forces['Story']== lower_floor) & (column_forces['Station']==max_station)]

    # merge side by side to get difference
    column_forces2 = column_forces_lower.merge(column_forces_upper[["Column", "Story", "P"]], how="outer", on="Column")


    # replace nan with 0
    column_forces2['P_y'] = column_forces2['P_y'].fillna(0)
    column_forces2['P_x'] = column_forces2['P_x'].fillna(0)

    # replace 'nan' story_x for pillars that are transferred
    column_forces2['Story_x'] = column_forces2['Story_x'].fillna(lower_floor)

    # get difference as load to consider to punching shear
    column_forces2["Axial Diff"] = column_forces2['P_y']-column_forces2['P_x']


    # round "Axial Diff" column
    decimals = 2
    column_forces2["Axial Diff"] = column_forces2["Axial Diff"] .apply(lambda x: round(x, decimals))

    #sort values in decreasing order
    column_forces2 = column_forces2.sort_values(by="Axial Diff", ascending = False)

    # add design section column
    column_forces2 = column_forces2.merge(frame_assignments[["Unique Name", "Design Section"]], how="left", on="Unique Name")

    # get just the columns we need
    column_forces2 = column_forces2[['Column', 'Design Section', 'P_x', 'Axial Diff',]]

    # rename columns to improve readability and join dataframes later
    column_forces2.rename(columns={'Axial Diff': 'Axial Diff - ' + lower_floor,
                                   'Design Section': 'Design Section - ' + lower_floor,
                                   'P_x': 'P - ' + lower_floor,
                                   }, inplace=True)
    
    # export dataframe to excel
    #column_forces2.to_excel(upper_floor + "_" + lower_floor + "_" + "AxialDiff.xlsx")

    return column_forces2


