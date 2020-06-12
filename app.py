from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
import requests
from flask import json
import json

def get_age(age):
    if(age<=5):
        age = 1
    elif(age>5 and age<=10):
        age = 2
    elif (age > 10 and age <= 15):
        age = 3
    elif (age > 15 and age <= 20):
        age = 4
    elif (age > 20 and age <= 25):
        age = 5
    elif (age > 25 and age <= 30):
        age = 6
    elif (age > 30 and age <= 35):
        age = 7
    elif (age > 35 and age <= 40):
        age = 8
    elif (age > 40 and age <= 45):
        age = 9
    elif (age > 45 and age <= 50):
        age = 10
    elif (age > 50 and age <= 55):
        age = 11
    elif (age > 55 and age <= 60):
        age = 12
    elif (age > 60 and age <= 65):
        age = 13
    elif (age > 65 and age <= 70):
        age = 14
    elif (age > 70 and age <= 75):
        age = 15
    elif (age > 75 and age <= 80):
        age = 16
    elif (age > 80 and age <= 85):
        age = 17
    elif (age > 85 and age <= 90):
        age = 18
    elif (age > 90):
        age = 19
    return age

def getToken():
    payload = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'apikey':'TQGmHVIV-9RwAeU1W23k3Mb-0zGXozuRdxjs9-AMrfP2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    url = 'https://iam.bluemix.net/identity/token'
    response = requests.post(url, data=payload, verify=False)
    data  = json.loads(response.text)
    return data['access_token']


def makeRequest(value, token):
    header = {'Content-Type': 'application/json', 'cache-control': 'no-cache', 'Authorization': 'Bearer '
               + token,
              'ML-Instance-ID': "358eb886-1ef8-4e27-ba14-1d8e7b7270e7"}

    response_scoring = requests.post(
                "https://us-south.ml.cloud.ibm.com/v4/deployments/ddd87cfc-b39e-4d31-b19b-025accedf89e/predictions",
        json=value, headers=header)
    status = str(response_scoring.status_code)
    output = json.loads(response_scoring.text)
    print(status)

    if status.startswith('4'):
        token = getToken()
        makeRequest(value,token)

    return  output


app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key'

@app.before_first_request
def _run_on_start():
    _run_on_start.first_token = str(getToken())

@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)


@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():


        if(form.antigen.data == None):
          python_object = []
        else:
          python_object = [int(form.patient_age_quantile.data), int(form.patient_addmited_to_regular.data),
                           int(form.patient_addmited_to_semi_intense.data), int(form.patient_addmited_to_intense.data),
                           float(form.platelets.data), float(form.mean_platelet_volume.data), float(form.red_blood_cells.data),
                           float(form.lymphocytes.data), float(form.mean_corpuscular_hemoglobin_concentration.data),
                           float(form.leukocytes.data), float(form.basophils.data), float(form.eosinophils.data),
                           float(form.mean_corpuscular_volum.data), float(form.monocytes.data),
                           float(form.red_blood_cell_distribution_width.data), int(form.antigen.data)]

        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # # NOTE: manually define and pass the array(s) of values to be scored in the next line
        test_value = {"input_data": [{"fields": ["patient_age_quantile", "patient_addmited_to_regular",
          "patient_addmited_to_semi_intense", "patient_addmited_to_intense", "platelets", "mean_platelet_volume",
          "red_blood_cells", "lymphocytes", "mean_corpuscular_hemoglobin_concentration",
          "leukocytes", "basophils", "eosinophils", "mean_corpuscular_volum",
          "monocytes", "red_blood_cell_distribution_width", "antigen"], "values": userInput }]}

        test_value["input_data"][0]["values"][0][0] = get_age(int(test_value["input_data"][0]["values"][0][0]))
        print(test_value)


        output = makeRequest(test_value, _run_on_start.first_token)


        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]


        if(bc[0][0]==0):
            result = "Negative to Covid-19 Test"
            confident = "Condifident of : "+str(round(bc[0][1][0],3))
        else:
            result = "Positve to Covid-19 Test "
            confident = "Condifident of : " + str(round(bc[0][1][1],3))


        print(result)
  
        form.abc = result
        form.confi = confident
        return render_template('index.html', form=form)

if __name__ == "__main__":
  app.run(debug=True)