from flask import Flask, render_template, request, url_for, redirect, session, jsonify
import re
from flask import send_file
import pandas as pd
import pickle
from connection import *
import sqlite3

app = Flask(__name__)
app.secret_key = "zxsdasdasdasdsd"
app.teardown_appcontext(close_db)

@app.before_request
def initialize():
    create_table()
    
# Load your data
df_1 = pd.read_csv("../Project/Telco-Customer-Churn-Prediction/first_telc.csv")

@app.route("/")
def index():
    if 'username' in session:
        return render_template('index.html', query="")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        print()
        if user:
            session['username'] = user['name']
            session['email'] = user['email']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password', email=email, password=password)
    return render_template('login.html', email='', password='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not is_valid_name(name) or not is_gmail_address(email) or not is_strong_password(password):
            return render_template('register.html', error='Please ensure all fields are valid.', name=name, email=email, password=password)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            return render_template('register.html', error='Email already exists.', name=name, email=email, password=password)

        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html', name='', email='', password='')

def is_valid_name(name):
    # Name should contain only alphabets and spaces
    return bool(re.match("^[a-zA-Z ]+$", name))


def is_gmail_address(email):
    # Check if the email ends with @gmail.com
    return email.endswith("@gmail.com")


def is_strong_password(password):
    # Check for minimum length of 6, include upper, lower and digits
    if len(password) < 6:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'username' not in session:
          return redirect(url_for('login'))
        '''
        SeniorCitizen
        MonthlyCharges
        TotalCharges
        gender
        Partner
        Dependents
        PhoneService
        MultipleLines
        InternetService
        OnlineSecurity
        OnlineBackup
        DeviceProtection
        TechSupport
        StreamingTV
        StreamingMovies
        Contract
        PaperlessBilling
        PaymentMethod
        tenure
        '''
        inputQuery1 = request.form['SeniorCitizen']
        inputQuery2 = request.form['MonthlyCharges']
        inputQuery3 = request.form['TotalCharges']
        inputQuery4 = request.form['Gender']
        inputQuery5 = request.form['Partner']
        inputQuery6 = request.form['Dependents']
        inputQuery7 = request.form['PhoneService']
        inputQuery8 = request.form['MultipleLines']
        inputQuery9 = request.form['InternetService']
        inputQuery10 = request.form['OnlineSecurity']
        inputQuery11 = request.form['OnlineBackup']
        inputQuery12 = request.form['DeviceProtection']
        inputQuery13 = request.form['TechSupport']
        inputQuery14 = request.form['StreamingTV']
        inputQuery15 = request.form['StreamingMovies']
        inputQuery16 = request.form['Contract']
        inputQuery17 = request.form['PaperlessBilling']
        inputQuery18 = request.form['PaymentMethod']
        inputQuery19 = request.form['tenure']
    
    
        data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, 
                inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12, inputQuery13, inputQuery14,
                inputQuery15, inputQuery16, inputQuery17, inputQuery18, inputQuery19]]
        new_df = pd.DataFrame(data, columns = ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
                                            'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
                                            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                            'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                                            'PaymentMethod', 'tenure'])
        df_2 = pd.concat([df_1, new_df], ignore_index = True) 
        # Group the tenure in bins of 12 months
        labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
        
        df_2['tenure_group'] = pd.cut(df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels)

        #drop column tenure
        df_2.drop(columns= ['tenure'], axis=1, inplace=True) 
        df_2.SeniorCitizen = pd.to_numeric(df_2.SeniorCitizen, errors='coerce')
        df_2.MonthlyCharges = pd.to_numeric(df_2.MonthlyCharges, errors='coerce')
        df_2.TotalCharges = pd.to_numeric(df_2.TotalCharges, errors='coerce')
        
        new_df__dummies = pd.get_dummies(df_2[['gender', 'SeniorCitizen','MonthlyCharges', 'TotalCharges', 'Partner', 'Dependents', 'PhoneService',
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
            'Contract', 'PaperlessBilling', 'PaymentMethod','tenure_group']])
    
        # Load model
        model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modeldt.sav", "rb"))
        # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modellog.sav", "rb"))
        # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelrf.sav", "rb"))
        # model = pickle.load(open("../Project/Telco-Customer-Churn-Prediction/modelsvm.sav", "rb"))

        single = model.predict(new_df__dummies.tail(1))
        
        if single==1:
             try:
                 InsertPredictionsData(inputQuery4,inputQuery5,inputQuery6,inputQuery7,inputQuery8,inputQuery9,inputQuery10,inputQuery11,inputQuery12,inputQuery13,inputQuery14,inputQuery15,inputQuery16,inputQuery17,inputQuery18,inputQuery2,inputQuery3,inputQuery19, "Churn")
                 result = "This customer is churned!!."
                 return jsonify(message=result)
             except Exception as e:
                 return jsonify(message=str(e)), 500
           
        else:
            try:
                InsertPredictionsData(inputQuery4,inputQuery5,inputQuery6,inputQuery7,inputQuery8,inputQuery9,inputQuery10,inputQuery11,inputQuery12,inputQuery13,inputQuery14,inputQuery15,inputQuery16,inputQuery17,inputQuery18,inputQuery2,inputQuery3,inputQuery19, "Not churn")
                result = "This customer is not churn."
                return jsonify(message=result, data=data)
            except Exception as e:
                 return jsonify(message=str(e)), 500
            
    elif request.method == 'GET':
        
        return render_template('index.html')
    return 'Bad Request!', 400


@app.route('/api/statistics')
def get_statistics():
    data_table = SummarizePrediction("table")
    data_churn = SummarizePrediction("churn")
    data_not_churn = SummarizePrediction("not churn")

    table_data = [dict(row) for row in data_table] if data_table else []

    stats_data = {
        'total_data': len(data_table) if data_table else 0,
        'total_churn': len(data_churn) if data_churn else 0,
        'total_not_churn': len(data_not_churn) if data_not_churn else 0
    }

    return jsonify({
        'statistics': stats_data,
        'tableData': table_data
    })

@app.route('/download-excel')
def download_excel():
    conn = get_db()  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[column[0] for column in cursor.description])

    excel_path = 'C:/Users/Zakar/Desktop/THESIS/Project/Telco-Customer-Churn-Prediction/predictions.xlsx'
    df.to_excel(excel_path, index=False, engine='openpyxl')

    return send_file(excel_path, as_attachment=True, download_name='Predictions.xlsx')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        create_table()
        create_predictinTable()    
    app.run(debug=True)




