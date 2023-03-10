# Etabs_tables_manipulation
## Data manipulation tools using python/pandas applied to Etabs exported excel tables

### Objective ###
To leverage python data analysis tools to extract organised information from exported Etabs tables (in Excel format).

---------
### 1.0 Punching Shear Loads Scripts ###
Outputs an Excel Table with Punching Shear loads by Column Label and by floor

**SlabPunShearLoad_rev1.py** (main script) - Reads Excel tables exported from Etabs and runs GetAxialForceDiff.py script for each floor for punching shear load; runs also for just one floor models

**GetAxialForceDiff_rev4.py** (function definition) - Gets column axial force difference between two story levels (punching shear for slab)

--------
### 2.0 Column Design Scripts ###
**ColumnRebarPercentage.py** - Gets rebar percentage for all rectangular RC column sizes in a model

--------
### 3.0 Beam Design Scripts ###
Reads Excel tables exported from Etabs and Outputs an Excel Table with flexural rebar reinforcement capacity utilization information for one beam.

3. **BeamAnalysisAndDesign_rev2.py** (main script) - Reads Excel tables exported from Etabs and Outputs an Excel Table with flexural rebar reinforcement capacity utilization information for one beam.
   - 3.1 **ImportExcelTables.py** - Imports Excel tables exported from Etabs
   - 3.2 **BeamForces_rev7.py** - gets beam internal forces from Etabs table
         - 3.2.1 **find_nearest.py** - gets Etabs beam station nearest to station user inputs 
         - 3.2.2 **MaxBeamForces_rev1.py** - 
    

TO BE COMPLETED
