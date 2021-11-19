import os

import numpy as np
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

imgFolder = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = imgFolder

def classify(data):
    data = np.array([data])
    model = open('model.pkl', 'rb')
    return joblib.load(model).predict(data)

@app.route('/')
def home():
    img = os.path.join(app.config['UPLOAD_FOLDER'], 'welcome-to-fraud.jpg')
    return render_template('index.html', image= img)

@app.route('/prediction', methods= ['POST'])
def prediction():
    type_transaction = request.form.get('type')
    amount = request.form.get('amount')
    oldbalanceOrg = request.form.get('oldbalanceOrg')
    newbalanceOrg = request.form.get('newbalanceOrg')
    oldbalanceDest = request.form.get('oldbalanceDest')
    newbalanceDest = request.form.get('newbalanceDest')
    data = [type_transaction, amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest]
    try: 
        result = classify([float(i) for i in data])
        if result[0] == 0: 
            predict = 'This is not a fraud'
            img = os.path.join(app.config['UPLOAD_FOLDER'], 'let-the-fraud-flow-through-you.jpg')
        else: 
            predict = 'This is a fraud'
            img = os.path.join(app.config['UPLOAD_FOLDER'], 'fraud-detected.jpg')
        return render_template('prediction.html', prediction = predict, image= img)
    except:
        return 'Enter a valid value'

if __name__ == '__main__':
    app.run(debug= True)