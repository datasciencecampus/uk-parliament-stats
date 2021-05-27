# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:53:00 2021

@author: corber
"""

import spacy
from spacy.tokens import DocBin
import string
from sklearn.model_selection import train_test_split


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
doc_bin.to_disk("outputs/spacy/debate_train.spacy")

validation_docs = make_docs(debate_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("outputs/spacy/debate_validation.spacy")

#Training/Validation data - Debate (cleaned) only
train_docs = make_docs(debate_cleaned_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("outputs/spacy/debate_cleaned_train.spacy")

validation_docs = make_docs(debate_cleaned_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("outputs/spacy/debate_cleaned_validation.spacy")


#Training/Validation data - Speech only
train_docs = make_docs(speech_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("outputs/spacy/speech_train.spacy")

validation_docs = make_docs(speech_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("outputs/spacy/speech_validation.spacy")

#Training/Validation data - Debate & Speech combined
train_docs = make_docs(combined_training_data)
doc_bin = DocBin(docs = train_docs)
doc_bin.to_disk("outputs/spacy/combined_train.spacy")

validation_docs = make_docs(combined_validation_data)
doc_bin = DocBin(docs = validation_docs)
doc_bin.to_disk("outputs/spacy/combined_validation.spacy")