# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:17:20 2021

@author: corber

Issues:
    - what if >1 item in single speech? Should this be counted multiple times?

Next steps:
    - find location of match & take 50 words before/after as short context for dashboard
        -> what if multiple matches?
    - tf-idf for topic -> do this by debate title or speeches within debates?

"""


# --- Libraries ---
import pandas as pd
import matplotlib.pyplot as plt


# --- Variables ---

#parliament speech data
inputfile = "data/commonsdebates_2015_2019-utf8.csv"

#keywords to search for in speeches
keywords = ["ONS","Office for National Statistics", "Office of National Statistics", "UKSA", "UK Statistics Authority", "OSR", "Office for Statistics Regulation", "Office of Statistics Regulation"]

# --- Analysis ---
df = pd.read_csv(inputfile)

#group keywords together, use '|' to separate and allow str.contains function to parse as logical OR (function accepts regex pattern)
keywords_combined = '|'.join(keywords)

#create T/F flag in 'match' for any speeches that contain keywords - case sensitive (as otherwise 'ons' will match on a LOT).
df["match"] = df["text"].str.contains(keywords_combined)

#filter df to only contain rows with mentions
matchedrows = df[df["match"] == True]

#convert date from object to datetime
matchedrows["date"] = pd.to_datetime(matchedrows["date"])

#extract year & week from the date
matchedrows["year"] = matchedrows["date"].dt.year
matchedrows["weeknum"] = matchedrows["date"].dt.week

#force two figures in weeknum, e.g. '5' -> '05', so that ordering can be done using week var created below
matchedrows["weeknum"] = matchedrows["weeknum"].apply(lambda x: '{0:0>2}'.format(x))

#create year specific week variable (e.g. 2015-03)
matchedrows["week"] = matchedrows["year"].astype(str) + "-" + matchedrows["weeknum"].astype(str)

#pull out context of mention from speech - take 200 characters either side 

#find character location of key word
matchedrows["keyword_location"] = matchedrows["text"].str.find("Office for National Statistics")

#create start/stop character locations for extracting context, cap at 0 & max length of str
matchedrows["context-start"] = matchedrows["keyword_location"]-200
matchedrows["context-stop"] = matchedrows["keyword_location"]+200

matchedrows.loc[matchedrows["context-start"] < 0, 'context-start'] = 0
matchedrows.loc[matchedrows["context-stop"] > matchedrows["text"].str.len(), 'context-stop'] = matchedrows["text"].str.len()

#slice string based on start/stop values to extract context
matchedrows["context"] = matchedrows["text"].str.slice(start = matchedrows["context-start"], stop = matchedrows["context-stop"]) ##doesn't work, returns nan
matchedrows["context"] = matchedrows["text"].str.slice(start = 3136, stop = 3536) ##this works (have tried several values here - where its out of range it returns an empty string). so problem must be with reading in the values from the start/stop columns?



# matchedrows["keyword_location"] = matchedrows["text"].str.findall(keywords_combined) ##this returns keywords that have been found in list

# matchedrows["text-split"] = matchedrows["text"].str.split(" ") ##splits speech out into list of words - not ideal though, if keyword we're after is followed by punctuation it won't work?



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
