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


print([t for t in nlp("This is a debate about the Criminal Justice system.")])