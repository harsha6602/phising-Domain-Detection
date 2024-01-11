# app.py
from flask import Flask , render_template ,request
import requests
# import last_logic_backup
import web_scarping.Feature_extraction_ff1 as fex
import pickle
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
model = tf.keras.models.load_model("model.h5")
# model = pickle.load(open("model.h5","rb"))

@app.route("/")
def home():
    return render_template('real_index1.html')


@app.route('/check_phishing', methods=['GET', 'POST'])
def check_phishing():
    if request.method == 'POST':
        domain = request.form['url']
        if "." not in domain:
            return render_template('real_result.html', result="invalid")
        if "www." in domain:
            domain = domain[4:]
        else:
            pass
        print(domain)
        url = "https://" + domain
        response = requests.get(url)
        if response.status_code == 200:

            new_url_features = fex.data_set_list_creation(domain)

            new_url_features = [new_url_features]

            prediction = model.predict(new_url_features)
            print(prediction)
            if prediction >= 0.5:
                print("The URL  is predicted as a phishing URL.")
                result = "The URL  is predicted as a phishing URL."

            else:
                print("The URL  is predicted as a legitimate URL.")
                result = "The URL  is predicted as a legitimate URL."
            return render_template('real_result.html', result=result)
        else:
            return render_template('real_result.html', result="not active")

    
if __name__=='__main__':
    app.run(debug=True)