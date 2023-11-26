from cohortextractor import codelist, codelist_from_csv

##### Diabetes        
# T2DM
diabetes_t2_codes = codelist_from_csv(
    "codelists/opensafely-type-2-diabetes.csv", 
    system="ctv3", 
    column="CTV3ID"
)

##### Medications
# Metformin
metformin_med_codes = codelist_from_csv(
    "codelists/user-john-tazare-metformin-dmd.csv",
    system="snomed",
    column="dmd_id"
)