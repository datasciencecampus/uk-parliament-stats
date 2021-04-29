# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:49:54 2021

@author: corber


Identifying topics of each debate using a rules-based approach

Topics suggested by Millie Tyler:
    
Census
Health
COVID-19
Population and Migration
Economy
Labour Market
Crime
Environment
Inequalities/Wellbeing

"""

# --- Libraries ---

import pandas as pd
import spacy
from spacy.matcher import Matcher


# --- Variables ---

#parliament speech dataset
inputfile = "data/commonsdebates_2015_2019-utf8.csv"



# --- Data Prep ---

# create dataframe
df = pd.read_csv(inputfile)

# cut down to one row per debate & take 10% sample of this -> use seed so re-running during development is consistent
df = df.drop_duplicates(subset=['agenda']).sample(frac=0.1, random_state=1)


# set up nlp pipeline
nlp = spacy.load("en_core_web_md")



# --- Topic Classification --- 
#ideas: NER for countries -> foreign policy (excl. UK/Wales/Scotland/NI obv)

# -- Patterns for matching --

#Census
patterns_census = [
[{'LOWER': 'census'}]
    ]

#Health
patterns_health = [
[{'LOWER': 'health'}],
[{'LOWER': 'nhs'}],
[{'LOWER': 'hospital'}],
[{'LOWER': 'illness'}],
[{'LOWER': 'disease'}]
    ]

#COVID-19 - not in 2015-2019 dataset

#Population and Migration
patterns_popmigration = [
[{'LOWER': 'migration'}],
[{'LOWER': 'migrant'}],
[{'LOWER': 'immigration'}],
[{'LOWER': 'population'}]
    ]


#Economy
patterns_economy = [
[{'LOWER': 'gdp'}],
[{'LOWER': 'borrow'}],
[{'LOWER': 'finance'}]
    ]

#Labour Market
patterns_labourmarket = [
[{'LOWER': 'job'}],
[{'LOWER': 'employment'}],
[{'LOWER': 'employee'}],
[{'LOWER': 'employer'}]
    ]

#Crime
patterns_crime = [
[{'LOWER': 'crime'}],
[{'LOWER': 'criminal'}],
[{'LOWER': 'police'}],
[{'LOWER': 'prison'}],
[{'LOWER': 'court'}],
[{'LOWER': 'offence'}]
    ]


#Environment
patterns_environment = [
[{'LOWER': 'environment'}],
[{'LOWER': 'green'}],
[{'LOWER': 'carbon'}],
[{'LOWER': 'fossil'}],
[{'LOWER': 'oil'}],
[{'LOWER': 'gas'}],
[{'LOWER': 'electric'}],
[{'LOWER': 'coal'}],
#net zero?
    ]

#Inequalities/Wellbeing
patterns_inequalwellbeing = [
[{'LOWER': 'equal'}],
[{'LOWER': 'wellbeing'}],
[{'LOWER': 'minority'}],
[{'LOWER': 'lgbt'}],
    ]


# -- Set up matcher in pipeline --
matcher = Matcher(nlp.vocab, validate=True)
matcher.add("CRIME", patterns_crime)


# -- Matching --

# function for finding matches
def get_matches(text):
    doc = nlp(text)
    matcher(doc)
    for match_id in matcher(doc):
        return doc.vocab.strings[match_id]
    return 'OTHER'

# identify topics from debate title
df['topic'] = df["agenda"].apply(lambda x : get_matches(x))


# -- Evaluate output, % in each topic, samples from each topic -- 


    