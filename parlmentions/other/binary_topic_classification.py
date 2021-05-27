# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:04:22 2021

@author: corber
"""
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