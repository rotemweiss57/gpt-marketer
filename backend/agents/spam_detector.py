import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("emails.csv")

# Preprocess text data
df["text"] = df["text"].str.lower()
df["text"] = df["text"].apply(word_tokenize)
stop_words = set(stopwords.words("english"))
df["text"] = df["text"].apply(lambda x: [word for word in x if word not in stop_words])
df["text"] = df["text"].apply(lambda x: " ".join(x))

# Feature Extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])

# Split the Dataset
X_train, X_test, y_train, y_test = train_test_split(X, df["spam"], test_size=0.2, random_state=42)

# Train a classification model, such as Multinomial Naive Bayes
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Evaluate the model's performance using metrics like accuracy and classification report
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
# print(report)

joblib.dump(classifier, 'email_spam_model.pkl')
loaded_model = joblib.load('email_spam_model.pkl')

text = ["Subject: EXCLUSIVE OFFER JUST FOR YOU!!! UNBELIEVABLE DISCOUNTS INSIDE Dear Valued Customer,"
        "You've been SELECTED to receive an EXCLUSIVE one-time offer! Our BIGGEST SALE EVER is here, "
        "and we're giving you the chance to SAVE UP TO 90% on our top products!!! Don't miss out on these "
        "once-in-a-lifetime deals! CLICK HERE NOW to unlock your special discount! But hurry, this offer is "
        "only valid for the next 24 HOURS! Stock is LIMITED, and these deals won't last long! Get the latest,"
        " most sought-after gadgets at a fraction of the price! Exclusive deals on luxury items you won't find "
        "anywhere else! And much, much more! Don't miss this opportunity to save like never before. Act NOW and "
        "be part of the lucky few who take advantage of our biggest sale of the year! Best Regards, The Deals "
        "Team P.S. Remember, these deals are too good to miss and won't be around for long."]
new_email = vectorizer.transform(text)
prediction = loaded_model.predict(new_email)

if prediction[0] == 1:
    print("This email is spam.")
else:
    print("This email is not spam.")