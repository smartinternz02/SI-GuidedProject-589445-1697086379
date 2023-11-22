import numpy as np
import pickle
# import joblib 
# import matplotlib
# import matplotlib.pyplot as plt 
# import time
import pandas as pd
# import os 
from flask import Flask , request, render_template

app = Flask(__name__)


model = pickle.load(open('rainfall.pkl','rb')) 
scale = pickle.load(open('scale.pkl','rb'))


@app.route('/')# route to display the home page 
def home(): 
  with app.app_context():
    return render_template('index.html') #rendering the home page
@app.route('/predict', methods=["POST", "GET"])# route to show the predictions in a web UI


def predict(): 
  with app.app_context():
    # reading the inputs given by the user
    input_feature=[x for x in request.form.values()]
    features_values=[np.array(input_feature)] 
    names = ['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed',
       'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
       'Pressure9am', 'Pressure3pm', 'Temp9am', 'Temp3pm', 'RainToday',
       'WindGustDir', 'WindDir9am', 'WindDir3pm', 'year', 'month', 'day']
    data = pd.DataFrame(features_values,columns=names)
    data = scale.fit_transform(data)
    data = pd.DataFrame(data, columns =names)
      # predictions using the loaded model file
    prediction=model.predict(data) 
    # pred_prob =model.predict_proba(data)
    print(prediction)
    if prediction == "Yes": 
        return render_template("Chance.html",prediction=prediction)
    else:
       return render_template("noChance.html",prediction=prediction) 
     

     #showing the prediction results in a UI 
     
# if __name__=="__main__":
if __name__ == '__main__':
    app.run(debug=True)
    # home()
    # predict()