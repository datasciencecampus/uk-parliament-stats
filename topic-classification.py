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
[{'LOWER': 'disease'}], # doesn't pick up 'diseases' with this - perhaps need to set up patterns as optional letter/keyword/optional letter ? --> probably need to lemmatize
[{'LOWER': 'diseases'}], 
[{'LOWER': 'disabled'}],
[{'LOWER': 'disability'}]
    ]

#COVID-19 - not in 2015-2019 dataset

#Population and Migration
patterns_popmigration = [
[{'LOWER': 'migration'}],
[{'LOWER': 'migrant'}],
[{'LOWER': 'immigration'}],
[{'LOWER': 'population'}],
[{'LOWER': 'refugee'}],
    ]


#Economy
patterns_economy = [
[{'LOWER': 'gdp'}],
[{'LOWER': 'borrow'}],
[{'LOWER': 'finance'}],
[{'LOWER': 'goods'}],
[{'LOWER': 'investment'}],
[{'LOWER': 'trading'}], #could make the case for some of these being under foreign policy?
[{'LOWER': 'trade'}],
[{'LOWER': 'product'}],
[{'LOWER': 'business'}],
[{'LOWER': 'tourism'}] 
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
[{'LOWER': 'offence'}],
[{'LOWER': 'prosecution'}],
    ]


#Environment
patterns_environment = [
[{'LOWER': 'environment'}],
[{'LOWER': 'climate'}],
[{'LOWER': 'green'}],
[{'LOWER': 'carbon'}],
[{'LOWER': 'fossil'}],
[{'LOWER': 'oil'}],
[{'LOWER': 'gas'}],
[{'LOWER': 'electric'}],
[{'LOWER': 'coal'}],
[{'LOWER': 'energy'}],
#net zero?
    ]

#Inequalities/Wellbeing
patterns_inequalwellbeing = [
[{'LOWER': 'equal'}],
[{'LOWER': 'wellbeing'}],
[{'LOWER': 'minority'}],
[{'LOWER': 'lgbt'}],
[{'LOWER': 'gender'}],
[{'LOWER': 'ethnic'}],
[{'LOWER': 'sexual'}], #possibly too broad to include in here? -> e.g. 'Sexual  Exploitation...'
    ]

# Education
patterns_education = [
[{'LOWER': 'school'}],
[{'LOWER': 'schools'}],
[{'LOWER': 'education'}],
[{'LOWER': 'teacher'}],
[{'LOWER': 'teachers'}],
[{'LOWER': 'learning'}]
    ]

# Transport
patterns_transport = [
[{'LOWER': 'transport'}],
[{'LOWER': 'transportation'}],
[{'LOWER': 'rail'}],
[{'LOWER': 'train'}],
[{'LOWER': 'railway'}],
[{'LOWER': 'bus'}],
[{'LOWER': 'plane'}],
[{'LOWER': 'airplane'}],
[{'LOWER': 'airport'}],
[{'LOWER': 'road'}],
[{'LOWER': 'roads'}],
[{'LOWER': 'motorway'}],
[{'LOWER': 'car'}],
[{'LOWER': 'driving'}]
    ]

# Military/Security

patterns_militarysecurity = [
[{'LOWER': 'war'}],
[{'LOWER': 'army'}], 
[{'LOWER': 'navy'}],
[{'LOWER': 'raf'}],
[{'LOWER': 'soldier'}],
[{'LOWER': 'soldiers'}],
[{'LOWER': 'veteran'}],
[{'LOWER': 'veterans'}],
[{'LOWER': 'military'}],
[{'LOWER': 'security'}],
[{'LOWER': 'cyber'}],
[{'LOWER': 'mi5'}],
[{'LOWER': 'mi6'}],
[{'LOWER': 'intelligence'}],
[{'LOWER': 'armed'}, {'LOWER': 'forces'}],
    ]


# Foreign Policy

patterns_foreignpolicy = [
[{'LOWER': 'eu'}],
[{'LOWER': 'european'}, {'lower': 'union'}],
[{'LOWER': 'withdrawal'}],
[{'LOWER': 'foreign'}],
    ]
#can use ENT: GPE to identify locations - but need to exclude domestic locations, how to do this?

# -- Set up matcher in pipeline --
matcher = Matcher(nlp.vocab, validate=True)
matcher.add("CENSUS", patterns_census)
matcher.add("HEALTH", patterns_health)
matcher.add("POPULATION_MIGRATION", patterns_popmigration)
matcher.add("ECONOMY", patterns_economy)
matcher.add("LABOURMARKET", patterns_labourmarket)
matcher.add("CRIME", patterns_crime)
matcher.add("ENVIRONMENT", patterns_environment)
matcher.add("INEQUAL_WELLBEING", patterns_inequalwellbeing)
matcher.add("EDUCATION", patterns_education)
matcher.add("TRANSPORT", patterns_transport)
matcher.add("MILITARY_SECURITY", patterns_militarysecurity)
matcher.add("FOREIGNPOLICY", patterns_foreignpolicy)


# -- Matching --

# function for finding matches -- ISSUE: only returns first match, doesn't handle text that may have more than 1 match
def get_matches(text):
    doc = nlp(text)
    matcher(doc)
    for match_id in matcher(doc):
        return doc.vocab.strings[match_id[0]] # match_id returns tuple of 3 ints: hashed ID, start, end (see: https://spacy.io/usage/spacy-101#vocab)
    return 'OTHER'

# identify topics from debate title
df['topic'] = df["agenda"].apply(lambda x : get_matches(x))

print(df['topic'].value_counts())



## Testing

#print sample of 'OTHER' debates to help update rules
df2 = df[df['topic'] == "OTHER"]
print(df2['agenda'].sample(10))

get_matches("the crime stats from the census") #test for multiple matches - not working atm

# -- Evaluate output, % in each topic, samples from each topic -- 


    