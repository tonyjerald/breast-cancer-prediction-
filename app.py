import numpy as np
import pandas as pd
import sqlite3
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
  return render_template('index.html')  

@app.route('/predict',methods=['POST'])
def predict():
  connection =  sqlite3.Connection("UsersDatabase.db")
  cursor= connection.cursor()
  cursor.execute("Create table UsersDatabase (clump_thickness real, uniform_cell_size real, uniform_cell_shape real, marginal_adhesion real, single_epithelial_size real, bare_nuclei real, bland_chromatin real, normal_nucleoli real, mitoses real, result text)")
  input_features = [float(x) for x in request.form.values()]
  features_value = [np.array(input_features)]
  features_name = ['clump_thickness', 'uniform_cell_size', 'uniform_cell_shape',
       'marginal_adhesion', 'single_epithelial_size', 'bare_nuclei',
       'bland_chromatin', 'normal_nucleoli', 'mitoses']
  
  df = pd.DataFrame(features_value, columns=features_name)
  output = model.predict(df)

  if output == 4:
      res_val = "Breast cancer"
  else:
      res_val = "no Breast cancer"
  input_features.append(res_val)
  features_tuple = tuple(input_features)
  cursor.execute("INSERT INTO UsersDatabase (clump_thickness, uniform_cell_size, uniform_cell_shape, marginal_adhesion, single_epithelial_size, bare_nuclei, bland_chromatin, normal_nucleoli, mitoses, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", features_tuple)
  connection.commit()
  connection.close()
  return render_template('index.html', prediction_text='Patient has {}'.format(res_val))

if __name__ == "__main__":
  app.run()
  
  
