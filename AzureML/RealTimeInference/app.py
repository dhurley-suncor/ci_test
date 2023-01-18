from flask import Flask, request
import numpy as np
import pickle

app = Flask(__name__)

# trigger workflow

linear_model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():

  payload = request.get_json(force=True)

  data = payload['data']

  value_to_predict = np.array([data]).reshape(-1, 1)

  prediction = linear_model.predict(value_to_predict)
  prediction = str(prediction[0][0])

@app.route('/info', methods=['GET'])
def predict():

  return "This is some information"
