import joblib


class SpamClassifier:
    def __init__(self, model_path='email_spam_model.pkl', vectorizer_path='vectorizer.pkl'):
        # Load the model and vectorizer at initialization
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def classify_email(self, email):
        # Transform the email using the loaded vectorizer
        transformed_email = self.vectorizer.transform([email])

        # Predict using the loaded model

        prediction = self.model.predict_proba(transformed_email)

        return prediction[0][1]  # Return percentage likelihood of being classified as spam

