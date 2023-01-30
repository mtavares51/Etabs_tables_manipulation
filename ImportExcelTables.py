import pandas as pd

def import_excel_tables(frame_assignments_excel, beam_forces_excel, frame_sections_excel, concrete_grade):
    '''imports etabs tables that were exported to excel'''
    '''returns beam_forces table that will input to design functions'''
    '''returns frame_count_df1 table that gives an overview of how many beams/sections we have in model'''
    '''returns frame_assignments - it is a list with all RC beams and etabs unique name'''



    # frame_assignments table
    frame_assignments = pd.read_excel(frame_assignments_excel, header=1)
    # drop units row
    frame_assignments = frame_assignments.drop(0)
    # select frame elements that are beams
    frame_assignments = frame_assignments[frame_assignments["Design Type"] == "Beam"]

    # beam_forces table
    beam_forces = pd.read_excel(beam_forces_excel, header=1)
    # drop units row
    beam_forces = beam_forces.drop(0)

    # frame_sections table
    frame_sections = pd.read_excel(frame_sections_excel, header=1)
    # drop units row
    frame_sections = frame_sections.drop(0)
    # add column with section names to join later
    frame_sections["Analysis Section"] = frame_sections["Name"]

    # add section assignment to forces table
    beam_forces1 = beam_forces.merge(frame_assignments[["Unique Name", "Analysis Section"]], how="left",
                                     on="Unique Name")

    # add material, depth and width to forces table
    beam_forces2 = beam_forces1.merge(frame_sections[["Analysis Section", "Material", "t3", "t2"]], how="left",
                                      on="Analysis Section")

    # create additional columns for maximum and minimum analysis
    beam_forces2['V2xT'] = beam_forces2['V2'] * beam_forces2['T']
    beam_forces2['V2xT'] = abs(beam_forces2['V2xT']) / sum(beam_forces2['V2xT']) * 100
    beam_forces2['abs(V2)'] = abs(beam_forces2['V2'])
    beam_forces2['abs(M3)'] = abs(beam_forces2['M3'])
    beam_forces2['abs(T)'] = abs(beam_forces2['T'])

    # count how many occurrences of beams are in the model
    frame_count_df = frame_assignments["Analysis Section"].value_counts().rename_axis('Analysis Section').reset_index(
        name='Counts')

    # merge material properties on frame_count table
    frame_count_df1 = frame_count_df.merge(frame_sections[["Analysis Section", "Material"]], how="left",
                                           on="Analysis Section")

    # filter RC beams (by concrete grade)
    rc_beams_df = frame_count_df1[frame_count_df1['Material'] == concrete_grade]
    rc_beams_list = list(rc_beams_df["Analysis Section"])

    # filter frame_assignments dataframe by RC beams
    frame_assignments = frame_assignments[frame_assignments["Analysis Section"].isin(rc_beams_list)]
    frame_assignments = frame_assignments.sort_values("Analysis Section")
    # export to excel
    frame_assignments.to_excel("beams_etabs_schedule.xlsx")

    return beam_forces2, frame_count_df1, frame_assignments



