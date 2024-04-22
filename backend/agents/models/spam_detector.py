import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib

nltk.download('punkt')

df = pd.read_csv("../emails.csv") # Load data

# Preprocess text data
df["text"] = df["text"].str.lower()
df["text"] = df["text"].apply(word_tokenize)
stop_words = set(stopwords.words("english"))
df["text"] = df["text"].apply(lambda x: [word for word in x if word not in stop_words])
df["text"] = df["text"].apply(lambda x: " ".join(x))

# Feature Extraction using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))  # Using bigrams along with unigrams
X = vectorizer.fit_transform(df["text"])
y = df["spam"]

# Split the Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a classification model
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Save the model and the vectorizer
joblib.dump(classifier, 'email_spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
