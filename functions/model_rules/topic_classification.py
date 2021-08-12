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



# set up nlp pipeline
nlp = spacy.load("en_core_web_md")
lemmatizer = nlp.get_pipe("lemmatizer")
matcher = Matcher(nlp.vocab, validate=True)

#for loop over items in patterns dictionary to add them to the matcher
for key, value in patterns.patterns_dict.items():
    matcher.add(key, value)




# -- Matching Functions --

# function for identifying a match on a piece of text -- ISSUE: only returns first match, doesn't handle text that may have more than 1 match
def get_matches(text):
    text_lowercase = text.lower() #force text to all lower case
    doc = nlp(text_lowercase) #convert text to nlp object
    rootdoc = lemmatizer(doc) #lemmatize the entire text
    matcher(rootdoc) #apply matching rules to lemmatized text
    for match_id in matcher(rootdoc):
        return rootdoc.vocab.strings[match_id[0]] # match_id returns tuple of 3 ints: hashed ID, start, end (see: https://spacy.io/usage/spacy-101#vocab)
    return 'OTHER'


# classifying debates in a dataframe by topic 
def classify_debates(df):
    #use matcher on dataframe supplied
    df_uniquedebates = df.drop_duplicates(subset=['agenda']) #create df with only unique debate titles - speeds up processing
    df_uniquedebates['topic'] = df_uniquedebates['agenda'].apply(lambda x : get_matches(x)) #identify matches row by row
    df_uniquedebates['topic'] = df_uniquedebates['topic'].str.replace('EXCEPTIONS', 'OTHER', case=True, regex=None) #recode exceptions into 'other' category
    output_df = df.merge(df_uniquedebates, on='agenda', suffixes=(None, "_dropme")) #join topics from unique debates onto full dataset, duplicate fields get '_dropme' suffix
    output_df = output_df.loc[:,~output_df.columns.str.contains('_dropme', case=False)] #drop duplicate fields create in join
    return output_df





    