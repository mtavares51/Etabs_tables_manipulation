import pandas as pd


'''Gets rebar percentage for all rectangular RC column sizes in a Etabs model

note: Concrete Frame Design must be run.
note: if copying this code to console, don't forget to make console directory same as excel tables location
and reload python console

'''

# etabs table to be exported: Model > Assignments > Frame Assignments > Frame Assignments - Summary
# input excel filename below
frame_assignments_excel = 'Etabs - frame assignments.xlsx'

# etabs table to be exported: Model>Definitions>Frame Sections>Frame Sections
# input excel filename below
frame_sections_excel = "Etabs - frame sections.xlsx"

# etabs table to be exported: Design > Concrete Design > Column Rebar Data
# input excel filename below
frame_rebar_excel = "Etabs - rebar data.xlsx"

# concrete grade of RC Column we want to design
concrete_grade = 'C30/37'

# frame_assignments table
frame_assignments = pd.read_excel(frame_assignments_excel, header=1)
frame_assignments = frame_assignments.drop(0)  # drop units row
frame_assignments = frame_assignments[frame_assignments["Design Type"] == "Column"]  # select column frames

# rebar table
frame_rebar = pd.read_excel(frame_rebar_excel, header=1)
frame_rebar = frame_rebar.drop(0)  # drop units row

# frame_sections table
frame_sections = pd.read_excel(frame_sections_excel, header=1)
frame_sections = frame_sections.drop(0)  # drop units row
frame_sections["Design Section"] = frame_sections["Name"]  # add column with section names to join later


# add material, depth and width to forces table
frame_rebar1 = frame_rebar.merge(frame_sections[["Design Section", "Material", "t3", "t2"]], how="left",
                                      on="Design Section")

# add column with section area
frame_rebar1["Area"] = frame_rebar1['t3']*frame_rebar1['t2']

# add column with rebar percentage (unit is percentage %)
frame_rebar1["Rebar Percentage"] = frame_rebar1['As']/frame_rebar1['Area']*100

# round column with rebar percentage
decimals = 2
frame_rebar1['Rebar Percentage'] = frame_rebar1['Rebar Percentage'].apply(lambda x: round(x, decimals))

# export dataframe to excel
frame_rebar1.to_excel("ColumnRebarData - " + frame_rebar_excel)




