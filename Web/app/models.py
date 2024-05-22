import pickle

class PredictiveModel:
    def __init__(self):
        self.model = pickle.load(open('app/model/model.pkl', 'rb'))

    def predict(self, features):
        return self.model.predict([features])
