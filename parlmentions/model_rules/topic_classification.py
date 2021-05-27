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
from parlmentions.model_rules import patterns
from spacy.matcher import Matcher



# --- Variables ---

#parliament speech dataset
inputfile = "raw-data/commonsdebates_2015_2019-utf8.csv"

#output location
outputfile = "outputs/data/uk_parl_stats.csv"


# --- Data Prep ---

# create dataframe
df_full = pd.read_csv(inputfile)

# set up nlp pipeline
nlp = spacy.load("en_core_web_md")
lemmatizer = nlp.get_pipe("lemmatizer")

# --- Topic Classification --- 

# -- Import patterns --
patterns_dict = {
 "EXCEPTIONS": patterns.patterns_exceptions,
 "CENSUS": patterns.patterns_census,
 "HEALTH": patterns.patterns_health,
 "POPULATION_MIGRATION": patterns.patterns_popmigration,
 "ECONOMY": patterns.patterns_economy,
 "LABOURMARKET": patterns.patterns_labourmarket,
 "CRIME": patterns.patterns_crime,
 "ENVIRONMENT": patterns.patterns_environment,
 "INEQUAL_WELLBEING": patterns.patterns_inequalwellbeing,
 "EDUCATION": patterns.patterns_education,
 "TRANSPORT": patterns.patterns_transport,
 "DEFENCE": patterns.patterns_defence,
 "FOREIGNPOLICY": patterns.patterns_foreignpolicy,
 "HOUSING": patterns.patterns_housing,
 "TAXSPEND": patterns.patterns_taxspend,
}


# -- Set up matcher in pipeline --
matcher = Matcher(nlp.vocab, validate=True)

#for loop over items in patterns dictionary to add them to the matcher
for key, value in patterns_dict.items():
    matcher.add(key, value)


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


#identify topics from debate title for full dataset
df_full_uniquedebates = df_full.drop_duplicates(subset=['agenda']) #create df with only unique debate titles
df_full_uniquedebates['topic'] = df_full_uniquedebates['agenda'].apply(lambda x : get_matches(x))
df_full_uniquedebates['topic'] = df_full_uniquedebates['topic'].str.replace('EXCEPTIONS', 'OTHER', case=True, regex=None) #recode exceptions into 'other' category

#join topics from unique debates to full dataset
df_full = df_full.merge(df_full_uniquedebates, on='agenda', suffixes=(None, "_dropme"))
#drop duplicate fields
output = df_full.loc[:,~df_full.columns.str.contains('_dropme', case=False)] 
#output to csv
output.to_csv(outputfile)





    