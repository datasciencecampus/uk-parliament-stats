# -*- coding: utf-8 -*-
"""
Code Snippets used in testing/development

Created on Tue May 25 14:07:05 2021

@author: corber
"""


#pre-processing for cases where default sequence can be lead to misclassification

#my function that doesn't seem to do anything to the text at the moment
def preprocessing(text):
    text_lowercase = text.lower()
    doc = nlp(text_lowercase)
    for token in doc:
        if token.text == "public" and doc[token.i].nbor().text == "house":  #public house - should be other not housing
            with doc.retokenize() as retokenizer:
                attrs = {"LEMMA": "publichouse"}
                retokenizer.merge(doc[token.i:token.i+1], attrs=attrs)

        # elif token.text == "house": #house of... (commons/lords etc.) - should be other not housing
        #     if doc[token.i].nbor().text == "of":
        #         with doc.retokenize() as retokenizer:
        #                 attrs = {"LEMMA": "houseof"}
        #                 doc = retokenizer.merge(doc[token.i:token.i+1], attrs=attrs)
        #     else:
        #         pass   
        # elif token.text == "social": #social work/workers - should be other not employment
        #     if doc[token.i].nbor().text == "work" or doc[token.i].nbor().text == "worker":
        #         with doc.retokenize() as retokenizer:
        #                 attrs = {"LEMMA": "socialwork"}
        #                 doc = retokenizer.merge(doc[token.i:token.i+1], attrs=attrs)
        #     else:
        #         pass
        else:
            pass
    return print([(idx,tok) for idx,tok in enumerate(doc)])      

      
#function that (mostly) works -- merges tokens together but includes too many tokens atm, i think because I haven't edited the 'while end < len(doc)' line?
def preprocess(doc):
    spans = []
    for word in doc[:-1]:
        if word.text != "public" and word.nbor(1).text != "house":
            continue
        start = word.i
        end = word.i + 1
        print(start,end)
        while end < len(doc):
            end += 1
        span = doc[start:end]
        print(span)
        spans.append(span)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
    return doc.text


#testing preprocessing functions
preprocessing("closure of public house things")

doc = nlp("closure of public house things")


preprocess(doc)

print([(idx,tok) for idx,tok in enumerate(doc)])

#------------------------------------------------

#print sample of 'OTHER' debates to help update rules

print(df2['agenda'].sample(10))

# -- Evaluate output, % in each topic, samples from each topic -- 
print(lemmatizer.mode)
lemtest = nlp("working flexibly")

for word in lemtest:
    print(word.lemma_)

#------------------------------------------------

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

#------------------------------------------------

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





