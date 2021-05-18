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
from spacy.tokens import DocBin
from spacy.matcher import Matcher
import string
from sklearn.model_selection import train_test_split


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
[{'LEMMA': 'sme'}], #SME acronym
[{'LEMMA': 'economy'}],
[{'LEMMA': 'borrow'}],
[{'LEMMA': 'finance'}],
[{'LEMMA': 'goods'}],
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
[{'OP': '!'}, {'LEMMA': 'social'}, {'LEMMA': 'work'}], #exclude 'social work'
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
[{'LEMMA': 'domestic'}, {'LEMMA': 'violence'}],
[{'LEMMA': 'witness'}],
[{'LEMMA': 'stop'}, {'LEMMA': 'and'}, {'LEMMA': 'search'}],
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
[{'LEMMA': 'recycle'}],
[{'LEMMA': 'fly'}, {'LEMMA': '-'}, {'LEMMA': 'tipping'}],
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
[{'LEMMA': 'warhead'}],
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
[{'OP': '!'}, {'LEMMA': 'public'}, {'LEMMA': 'house'}], #exclude 'public house'
[{'OP': '!'}, {'LEMMA': 'house'}, {'LEMMA': 'of'}], #exclude 'house of..' (e.g. house of commons, lords etc.)
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

# output sample of 200 - evaluating rules based approach
df_evaluation = df.sample(frac=0.2, random_state=1)
df_evaluation.to_excel("data/rules-based-approach--evaluation.xlsx")

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

# -- Splitting into training/validation data --

df_combined["combined_debate_speech"] = "<DEBATE> " + df_combined["agenda"] + " <SPEECH> " + df_combined["text"]

##cut out stopwords from debate title

#stopwords
stopwords = spacy.lang.en.stop_words.STOP_WORDS
# punctuation
punctuation = string.punctuation

def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stopwords and word not in punctuation ]

    #Convert to string
    stringoutput = " ".join(mytokens)

    # return preprocessed list of tokens
    return stringoutput

df_combined['agenda_cleaned'] = df_combined["agenda"].apply(lambda x : spacy_tokenizer(x))

#cut df down to relevant fields -> debate title + topic
df_debate_trainvalid = list(zip(df_combined.agenda, df_combined.topic))
df_debate_cleaned_trainvalid = list(zip(df_combined.agenda_cleaned, df_combined.topic))
df_speech_trainvalid = list(zip(df_combined.text, df_combined.topic))
df_combined_trainvalid = list(zip(df_combined.combined_debate_speech, df_combined.topic))
    
# - Set up training/test data for model -- 40% for validation / seed to keep consistent / shuffle to mix up debates
debate_training_data, debate_validation_data = train_test_split(df_debate_trainvalid, test_size=0.4, random_state=3, shuffle=True)
debate_cleaned_training_data, debate_cleaned_validation_data = train_test_split(df_debate_cleaned_trainvalid, test_size=0.4, random_state=3, shuffle=True)
speech_training_data, speech_validation_data = train_test_split(df_speech_trainvalid, test_size=0.4, random_state=3, shuffle=True)
combined_training_data, combined_validation_data = train_test_split(df_combined_trainvalid, test_size=0.4, random_state=3, shuffle=True)

#function to apply category labels based on topic 
def make_docs(data):
    docs = []
    for doc, topic in nlp.pipe(data, as_tuples=True):
            #list all possible topics    
            doc.cats["CENSUS"] = 0
            doc.cats["HEALTH"] = 0
            doc.cats["POPULATION_MIGRATION"] = 0
            doc.cats["ECONOMY"] = 0
            doc.cats["LABOURMARKET"] = 0
            doc.cats["CRIME"] = 0
            doc.cats["ENVIRONMENT"] = 0
            doc.cats["INEQUAL_WELLBEING"] = 0
            doc.cats["EDUCATION"] = 0
            doc.cats["TRANSPORT"] = 0
            doc.cats["DEFENCE"] = 0
            doc.cats["FOREIGNPOLICY"] = 0
            doc.cats["HOUSING"] = 0
            doc.cats["TAXSPEND"] = 0
            doc.cats["OTHER"] = 0
            #update value to 1 for relevant topic 
            doc.cats[topic] = 1 
            docs.append(doc)
    return (docs)



#Training/Validation data - Debate only
train_docs = make_docs(debate_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("data/spacy/debate_train.spacy")

validation_docs = make_docs(debate_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("data/spacy/debate_validation.spacy")

#Training/Validation data - Debate (cleaned) only
train_docs = make_docs(debate_cleaned_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("data/spacy/debate_cleaned_train.spacy")

validation_docs = make_docs(debate_cleaned_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("data/spacy/debate_cleaned_validation.spacy")


#Training/Validation data - Speech only
train_docs = make_docs(speech_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("data/spacy/speech_train.spacy")

validation_docs = make_docs(speech_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("data/spacy/speech_validation.spacy")

#Training/Validation data - Debate & Speech combined
train_docs = make_docs(combined_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("data/spacy/combined_train.spacy")

validation_docs = make_docs(combined_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("data/spacy/combined_validation.spacy")

#print sample of 'OTHER' debates to help update rules

print(df2['agenda'].sample(10))

get_matches("the crime stats from the census") #test for multiple matches - not working atm

# -- Evaluate output, % in each topic, samples from each topic -- 
print(lemmatizer.mode)
lemtest = nlp("working flexibly")

for word in lemtest:
    print(word.lemma_)

    