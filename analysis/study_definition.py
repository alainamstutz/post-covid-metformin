from datetime import datetime, timedelta
from cohortextractor import (
StudyDefinition, 
patients, 
codelist, 
codelist_from_csv, # NOQA
# filter_codes_by_category  
)

import numpy as np
# Change this number to one for which your scripts 
# successfully run on the dummy data
np.random.seed(123456)

from codelists import *

start_date  = "2020-09-01" # difference between index_date and start_date? Why not simply using index_date below?

def days_before(s, days):
    date = datetime.strptime(s, "%Y-%m-%d")
    modified_date = date - timedelta(days=days)
    return datetime.strftime(modified_date, "%Y-%m-%d")

study = StudyDefinition(
    # define default dummy data behaviour
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.7,
        },
   
    # define the study index date
    index_date = "2020-09-01", # difference between index_date and start_date?

    # define the study population
    population=patients.satisfying(
        # t2dm = 1 ??? Why - and feather dataset contains t2dm == FALSE and TRUE
        """
        has_follow_up 
        AND (sex = "M")
        AND imd > 0
        AND t2dm = 1 
        """
        ,
        has_follow_up=patients.registered_with_one_practice_between(
            "2019-09-01", "2020-09-01"
            ),  
        ),
    
################
##### Treatments
################
    metformin_3mths=patients.with_these_medications(
            metformin_med_codes,
            between=[days_before(start_date, 90), start_date],
            return_expectations={"incidence": 0.3},
            ),

#####################
##### Characteristics
#####################
    age=patients.age_as_of(
        f"{start_date}",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
            },
        ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        },
        ),

    region=patients.registered_practice_as_of(
        f"{start_date}",
        returning="nuts1_region_name",
        return_expectations={
                "rate": "universal",
                "category": {
                    "ratios": {
                        "North East": 0.1,
                        "North West": 0.1,
                        "Yorkshire and The Humber": 0.1,
                        "East Midlands": 0.1,
                        "West Midlands": 0.1,
                        "East": 0.1,
                        "London": 0.2,
                        "South East": 0.1,
                        "South West": 0.1,
                    },
                },
            },
        ),

    imd=patients.address_as_of(
        f"{start_date}",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
                "rate": "universal",
                "category": {
                    "ratios": {
                        "100": 0.1,
                        "200": 0.1,
                        "300": 0.1,
                        "400": 0.1,
                        "500": 0.1,
                        "600": 0.1,
                        "700": 0.1,
                        "800": 0.1,
                        "900": 0.1,
                        "1000": 0.1,
                    }
                },
            },
        ),

#####################    
##### T2DM population
#####################
    t2dm=patients.with_these_clinical_events(
            diabetes_t2_codes,
            on_or_before=f"{start_date}",
            date_format="YYYY-MM-DD",
            return_expectations={"incidence": 0.05},
            ) 
)
