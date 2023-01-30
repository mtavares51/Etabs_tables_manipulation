# Etabs_tables_manipulation
## Data manipulation tools using python/pandas applied to Etabs output excel tables

### Objective ###
To leverage python data analysis tools to extract organised information from exported Etabs tables (in Excel format).

### 1.0 Punching Shear Loads Scripts ###
Outputs an Excel Table with Punching Shear loads by Column Label and by floor

**SlabPunShearLoad_rev1.py** - Gets input excel tables and runs GetAxialForceDiff.py script for each floor for punching shear load; runs also for just one floor models

**GetAxialForceDiff_rev4.py** - Gets column axial force difference between two story levels (punching shear for slab)

   

### 2.0 Column Design Scripts ###
**ColumnRebarPercentage.py** - Gets rebar percentage for all rectangular RC column sizes in a model
