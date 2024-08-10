from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'history' not in session:
        session['history'] = []
    if 'selected_bot' not in session:
        session['selected_bot'] = 'Query Bot'
    return render_template('index.html', history=session['history'], selected_bot=session['selected_bot'])

@app.route('/select_bot', methods=['POST'])
def select_bot():
    session['selected_bot'] = request.form['selected_bot']
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    input_text = request.form['query']
    selected_bot = session['selected_bot']
    response = None

    if selected_bot == 'Query Bot':
        response = get_query_response(input_text)
    elif selected_bot == 'Differential Diagnosis Bot':
        response = get_differential_diagnosis(input_text)
    elif selected_bot == 'Differential Diagnosis Bot with User Details':
        user_details = {
            'age': request.form['age'],
            'gender': request.form['gender'],
            'symptoms_duration': request.form['symptoms_duration'],
            'medications': request.form['medications'],
            'medical_history': request.form['medical_history']
        }
        context = f"Age: {user_details['age']}, Gender: {user_details['gender']}, Symptoms duration: {user_details['symptoms_duration']} months, Medications: {user_details['medications']}, Medical history: {user_details['medical_history']}\nQuery: {input_text}"
        response = get_differential_diagnosis_with_context(context)

    if response:
        session['history'].append({'query': input_text, 'response': response})
    else:
        response = "No response received from the server."

    return render_template('index.html', history=session['history'], selected_bot=session['selected_bot'], response=response)

def get_query_response(input_text):
    try:
        response = requests.post('http://localhost:8000/disease_query/invoke', json={'input': {'question': input_text}})
        response.raise_for_status()
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

def get_differential_diagnosis(input_text):
    try:
        data = {'input': {'question': input_text}}
        response = requests.post('http://localhost:8000/diffrential_diagnosis/invoke', json=data)
        response.raise_for_status()
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

def get_differential_diagnosis_with_context(context):
    try:
        data = {'input': {'context': context}}
        response = requests.post('http://localhost:8000/diffrential_diagnosis_with_context/invoke', json=data)
        response.raise_for_status()
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)








