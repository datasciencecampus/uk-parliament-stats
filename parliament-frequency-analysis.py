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


# --- Analysis ---

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
plt.savefig("user-engagement/frequency-of-mentions.png", dpi = 150)
