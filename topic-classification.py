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
import numpy as np
import spacy
from spacy.matcher import Matcher


# --- Variables ---

#parliament speech dataset
inputfile = "data/commonsdebates_2015_2019-utf8.csv"

#manually classified debate list
manualtopics = "data/unmatched-debates--manual-topics.xlsx"



# --- Data Prep ---

# create dataframe
df = pd.read_csv(inputfile)

# cut down to one row per debate & take 10% sample of this -> use seed so re-running during development is consistent
df = df.drop_duplicates(subset=['agenda']).sample(frac=0.1, random_state=1)


# set up nlp pipeline
nlp = spacy.load("en_core_web_md")
lemmatizer = nlp.get_pipe("lemmatizer")



# --- Topic Classification --- 

# -- Patterns for matching --

#Census
patterns_census = [
[{'LEMMA': 'census'}]
    ]

#Health
patterns_health = [
[{'LOWER': 'nhs'}], #NHS acronym
[{'LOWER': 'gp'}], #GP acronym
[{'LEMMA': 'health'}],
[{'LEMMA': 'healthcare'}],
[{'LEMMA': 'hospital'}],
[{'LEMMA': 'illness'}],
[{'LEMMA': 'sick'}],
[{'LEMMA': 'cancer'}],
[{'LEMMA': 'care'}],
[{'LEMMA': 'disease'}],
[{'LEMMA': 'disabled'}],
[{'LEMMA': 'disability'}],
[{'LEMMA': 'vaccinate'}],
[{'LEMMA': 'vaccination'}],
[{'LEMMA': 'medicine'}],
[{'LEMMA': 'treatment'}],
[{'LEMMA': 'treat'}],
    ]

#COVID-19 - not in 2015-2019 dataset

#Population and Migration
patterns_popmigration = [
[{'LEMMA': 'migration'}],
[{'LEMMA': 'migrant'}],
[{'LEMMA': 'immigrant'}],
[{'LEMMA': 'immigration'}],
[{'LEMMA': 'population'}],
[{'LEMMA': 'refugee'}],
[{'LEMMA': 'visa'}],
    ]


#Economy
patterns_economy = [
[{'LOWER': 'gdp'}], #GDP acronym
[{'LOWER': 'sme'}], #SME acronym
[{'LEMMA': 'economy'}],
[{'LEMMA': 'borrow'}],
[{'LEMMA': 'finance'}],
[{'LEMMA': 'goods'}],
[{'LEMMA': 'investment'}],
[{'LEMMA': 'trade'}],
[{'LEMMA': 'product'}],
[{'LEMMA': 'business'}],
[{'LEMMA': 'tourism'}],
[{'LEMMA': 'market'}],
[{'LEMMA': 'export'}],
[{'LEMMA': 'import'}],
[{'LEMMA': 'industry'}],
    ]

#Labour Market
patterns_labourmarket = [
[{'LEMMA': 'job'}],
[{'LEMMA': 'employment'}],
[{'LEMMA': 'employee'}],
[{'LEMMA': 'employer'}],
[{'LEMMA': 'work'}],
[{'LEMMA': 'worker'}],
[{'LEMMA': 'redundancy'}],
    ]

#Crime
patterns_crime = [
[{'LEMMA': 'crime'}],
[{'LEMMA': 'criminal'}],
[{'LEMMA': 'police'}],
[{'LEMMA': 'prison'}],
[{'LEMMA': 'prisoner'}],
[{'LEMMA': 'court'}],
[{'LEMMA': 'offence'}],
[{'LEMMA': 'prosecution'}],
[{'LEMMA': 'criminal'}],
[{'LEMMA': 'offender'}],
[{'LEMMA': 'sentence'}],
[{'LEMMA': 'sentencing'}],
    ]


#Environment
patterns_environment = [
[{'LEMMA': 'environment'}],
[{'LEMMA': 'climate'}],
[{'LEMMA': 'green'}],
[{'LEMMA': 'carbon'}],
[{'LEMMA': 'fossil'}],
[{'LEMMA': 'oil'}],
[{'LEMMA': 'gas'}],
[{'LEMMA': 'electric'}],
[{'LEMMA': 'coal'}],
[{'LEMMA': 'solar'}],
[{'LEMMA': 'wind'}],
[{'LEMMA': 'energy'}],
[{'LEMMA': 'nature'}],
[{'LEMMA': 'natural'}],
    ]

#Inequalities/Wellbeing
patterns_inequalwellbeing = [
[{'LOWER': 'lgbt'}], #acronym LGBT
[{'LOWER': 'bme'}], #acronym BME
[{'LOWER': 'bame'}], #acronym BAME
[{'LEMMA': 'equal'}],
[{'LEMMA': 'equality'}],
[{'LEMMA': 'wellbeing'}],
[{'LEMMA': 'minority'}],
[{'LEMMA': 'gender'}],
[{'LEMMA': 'ethnic'}],
[{'LEMMA': 'ethnicity'}],
    ]

# Education
patterns_education = [
[{'LEMMA': 'school'}],
[{'LEMMA': 'education'}],
[{'LEMMA': 'educate'}],
[{'LEMMA': 'teacher'}],
[{'LEMMA': 'teach'}],
[{'LEMMA': 'learn'}],
[{'LEMMA': 'pupil'}],
[{'LEMMA': 'student'}],
[{'LEMMA': 'college'}],
[{'LEMMA': 'university'}],
    ]

# Transport
patterns_transport = [
[{'LOWER': 'main'}, {'LOWER': 'line'}],
[{'LEMMA': 'transport'}],
[{'LEMMA': 'transportation'}],
[{'LEMMA': 'rail'}],
[{'LEMMA': 'train'}],
[{'LEMMA': 'railway'}],
[{'LEMMA': 'bus'}],
[{'LEMMA': 'plane'}],
[{'LEMMA': 'airplane'}],
[{'LEMMA': 'airport'}],
[{'LEMMA': 'fly'}],
[{'LEMMA': 'road'}],
[{'LEMMA': 'motorway'}],
[{'LEMMA': 'car'}],
[{'LEMMA': 'drive'}]
    ]

# Defence

patterns_defence = [
[{'LOWER': 'raf'}], #acronym - RAF
[{'LOWER': 'armed'}, {'LOWER': 'forces'}],
[{'LOWER': 'air'}, {'LOWER': 'force'}],
[{'LEMMA': 'defence'}],
[{'LEMMA': 'war'}],
[{'LEMMA': 'army'}], 
[{'LEMMA': 'navy'}],
[{'LEMMA': 'soldier'}],
[{'LEMMA': 'veteran'}],
[{'LEMMA': 'military'}],
[{'LEMMA': 'security'}],
[{'LEMMA': 'cyber'}],
[{'LEMMA': 'intelligence'}],

    ]


# Foreign Policy

patterns_foreignpolicy = [
[{'LOWER': 'eu'}], #acronym - EU
[{'LEMMA': 'european'}, {'LEMMA': 'union'}],
[{'LEMMA': 'europe'}],
[{'LEMMA': 'withdrawal'}], #i.e. Withdrawal Agreement
[{'LEMMA': 'foreign'}],
    ]
#can use ENT: GPE to identify locations - but need to exclude domestic locations, how to do this?

# Housing

patterns_housing = [
[{'LEMMA': 'house'}],
[{'LEMMA': 'housing'}],
[{'LEMMA': 'landlord'}],
[{'LEMMA': 'tenant'}],
[{'LEMMA': 'rent'}],
[{'LEMMA': 'let'}],
[{'LEMMA': 'mortgage'}],
[{'LEMMA': 'tenant'}],
[{'LEMMA': 'accommodation'}],

    ]

# Tax & Public Spending

patterns_taxspend= [
[{'LEMMA': 'spending'}],
[{'LEMMA': 'tax'}],
[{'LEMMA': 'taxation'}],
[{'LEMMA': 'welfare'}],
[{'LEMMA': 'benefit'}],
    ]


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
matcher.add("DEFENCE", patterns_defence)
matcher.add("FOREIGNPOLICY", patterns_foreignpolicy)
matcher.add("HOUSING", patterns_housing)
matcher.add("TAXSPEND", patterns_taxspend)


# -- Matching --

# function for finding matches -- ISSUE: only returns first match, doesn't handle text that may have more than 1 match
def get_matches(text):
    text_lowercase = text.lower() #force text to all lower case
    doc = nlp(text_lowercase) #convert text to nlp object
    rootdoc = lemmatizer(doc) #lemmatize the entire text
    matcher(rootdoc) #apply matching rules to lemmatized text
    for match_id in matcher(rootdoc):
        return rootdoc.vocab.strings[match_id[0]] # match_id returns tuple of 3 ints: hashed ID, start, end (see: https://spacy.io/usage/spacy-101#vocab)
    return 'OTHER'

# identify topics from debate title
df['topic'] = df["agenda"].apply(lambda x : get_matches(x))

#output anything tagged as 'OTHER' to xlsx for review
df2 = df[df['topic'] == "OTHER"]
df2.to_excel("data/unmatched-debates.xlsx")

# bring in manually classified debates
df_manual = pd.read_excel(manualtopics, index_col=0)

#force topics to uppercase & replace nan with "OTHER"
df_manual["topic-manual"] = df_manual["topic-manual"].str.upper()
df_manual = df_manual["topic-manual"]
df_manual = df_manual.replace(np.nan, 'OTHER', regex=True)

#join manual topics into primary dataframe
df_combined = df.join(df_manual)

#where topic = OTHER & topic-manual != null then take topic manual value
def topic_overwrite(row):
    if (row["topic"] == "OTHER"):
        return row["topic-manual"]
    else:
        return row["topic"]
    
df_combined["topic"] = df_combined.apply(lambda row: topic_overwrite(row), axis=1)


print(df_combined['topic'].value_counts())



## Testing




#print sample of 'OTHER' debates to help update rules

print(df2['agenda'].sample(10))

get_matches("the crime stats from the census") #test for multiple matches - not working atm

# -- Evaluate output, % in each topic, samples from each topic -- 
print(lemmatizer.mode)
lemtest = nlp("working flexibly")

for word in lemtest:
    print(word.lemma_)

    