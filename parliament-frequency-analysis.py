# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:17:20 2021

@author: corber

Issues:
    - what if >1 item in single speech? Should this be counted multiple times?

Next steps:
    - Topic classification
    - Sentiment analysis

"""


# --- Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import spacy
import string
from spacy.lang.en import English
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# --- Variables ---

#parliament speech data
inputfile = "data/commonsdebates_2015_2019-utf8.csv"

#keywords to search for in speeches
keywords = ["ONS","Office for National Statistics", "Office of National Statistics", "UKSA", "UK Statistics Authority", "OSR", "Office for Statistics Regulation", "Office of Statistics Regulation"]

# --- Functions ---

#used to extract context around keyword
def context_slicer (row):
    return row["text"][row["context-start"]:row["context-stop"]]



# --- Data Prep ---

# create dataframe
df = pd.read_csv(inputfile)

# -- Cut down dataframe to only contain rows containing a keyword match

#group keywords together, use '|' to separate and allow str.contains function to parse as logical OR (function accepts regex pattern)
keywords_combined = '|'.join(keywords)

#create T/F flag in 'match' for any speeches that contain keywords - case sensitive (as otherwise 'ons' will match on a LOT).
df["match"] = df["text"].str.contains(keywords_combined)

#filter df to only contain rows with mentions
matchedrows = df[df["match"] == True]

# -- Dates & Week numbering

#convert date from object to datetime
matchedrows["date"] = pd.to_datetime(matchedrows["date"])

#extract year & week from the date
matchedrows["year"] = matchedrows["date"].dt.year
matchedrows["weeknum"] = matchedrows["date"].dt.week

#force two figures in weeknum, e.g. '5' -> '05', so that ordering can be done using week var created below
matchedrows["weeknum"] = matchedrows["weeknum"].apply(lambda x: '{0:0>2}'.format(x))

#create year specific week variable (e.g. 2015-03)
matchedrows["week"] = matchedrows["year"].astype(str) + "-" + matchedrows["weeknum"].astype(str)

# -- Extract context around keyword mention

#find character location of key word
matchedrows["keyword_location"] = matchedrows["text"].str.find("Office for National Statistics")

#create start/stop character locations for extracting context, cap at 0 & max length of str
matchedrows["context-start"] = matchedrows["keyword_location"]-200
matchedrows["context-stop"] = matchedrows["keyword_location"]+200

matchedrows.loc[matchedrows["context-start"] < 0, 'context-start'] = 0
matchedrows.loc[matchedrows["context-stop"] > matchedrows["text"].str.len(), 'context-stop'] = matchedrows["text"].str.len()

#slice string based on start/stop values to extract context
matchedrows["context"] = matchedrows.apply(lambda row: context_slicer(row), axis=1)


# --- Initial Exploration Analysis ---

#calculate mention frequency per week
mention_frequency = matchedrows.groupby(matchedrows["week"], as_index=False).size()

print(mention_frequency.head(20))

#calc mentions by party of speaker - proportional to party size?
print(matchedrows.groupby(matchedrows["party"]).size())

#calc mentions by speaker & sort descending
print(matchedrows.groupby(matchedrows["speaker"]).size().sort_values(ascending=False))

#calc mean/median speech length
print(df.groupby('match', as_index=False)['terms'].mean())
print(df.groupby('match', as_index=False)['terms'].median())

#plot mentions over time
mention_frequency.plot(x="week", y="size")

#save plot as .png - in user engagement folder
#no need to update this every time i run this script atm# plt.savefig("user-engagement/frequency-of-mentions.png", dpi = 150)


# --- Topic Classification ---

# classification - my use case not a simple binary classification as in dataquest example, will need to explore out to structure model - want to test each text against all topics and choose tag with most relevant topic/all above certain score.

# tokenize > stopword removal > lemmatization (root words) > 
# other: part of speech (noun, adj, verb etc.), entity detection (could this be useful for identifying specific statistical outputs?), dependency parsing (may be important for sentiment analysis?), 

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_md')


#stopwords
stopwords = spacy.lang.en.stop_words.STOP_WORDS
# punctuation
punctuation = string.punctuation

# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stopwords and word not in punctuation ]

    # return preprocessed list of tokens
    return mytokens

# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()

# - Create components for model

#bag of words
bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))

#tfidf vectorization
tfidf_vector = TfidfVectorizer(tokenizer = spacy_tokenizer)

#classification method
classifier = LogisticRegression()

#dataset - group by party into 'Con' column - as Con (1) or Other (0)
matchedrows.loc[matchedrows.party != 'Con', 'Con'] = 0
matchedrows.loc[matchedrows.party == 'Con', 'Con'] = 1


# - Set up training/test data for model
X = matchedrows['text'] # the features we want to analyze
ylabels = matchedrows['Con'] # the labels, or answers, we want to test against

X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.3)


# - Create pipeline
print("Creating pipeline...")
pipe = Pipeline([("cleaner", predictors()),
                 ('vectorizer', bow_vector),
                 ('classifier', classifier)])


# Run model with training datasets
print("Training model...")
pipe.fit(X_train,y_train)

# Evaluate model with test datasets
print("Testing model...")
predicted = pipe.predict(X_test)

# Model Accuracy
print("Logistic Regression Accuracy:",metrics.accuracy_score(y_test, predicted))
print("Logistic Regression Precision:",metrics.precision_score(y_test, predicted))
print("Logistic Regression Recall:",metrics.recall_score(y_test, predicted))
    
