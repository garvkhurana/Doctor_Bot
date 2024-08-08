import streamlit as st
import requests

st.title("Doctor Bot")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_bot' not in st.session_state:
    st.session_state.selected_bot = 'Query Bot'

with st.sidebar:
    st.write('**Select Bot:**')
    bot_options = ['Query Bot', 'Differential Diagnosis Bot', 'Differential Diagnosis Bot with User Details']
    st.session_state.selected_bot = st.selectbox('', bot_options, index=0)

    st.write('**Query History:**')
    for i, entry in enumerate(st.session_state.history):
        question = entry["query"]
        st.button(question, key=i, on_click=lambda q=question: show_chat(q))

def get_query_response(input_text):
    try:
        response = requests.post('http://localhost:8000/disease_query/invoke',
                                 json={'input': {'question': input_text}})
        response.raise_for_status()  
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def get_diffrential_diagnosis(input_text, user_details=None):
    try:
        data = {'input': {'question': input_text}}
        if user_details:
            data['input']['user_details'] = user_details
        response = requests.post('http://localhost:8000/diffrential_diagnosis/invoke',
                                 json=data)
        response.raise_for_status()  
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def get_diffrential_diagnosis_with_context(context):
    try:
        data = {'input': {'context': context}}
        response = requests.post('http://localhost:8000/diffrential_diagnosis_with_context/invoke',
                                 json=data)
        response.raise_for_status()  
        return response.json()["output"]
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def show_chat(question):
    for entry in st.session_state.history:
        if entry["query"] == question:
            st.write(f'**Query**: {entry["query"]}')
            st.write(f'**Response**: {entry["response"]}')

if st.session_state.selected_bot == 'Query Bot':
    input_text = st.text_input('## Write your query')
    if st.button('Search'):
        if input_text:
            response = get_query_response(input_text)
            if response:
                st.session_state.history.append({'query': input_text, 'response': response})
                st.write(response)

elif st.session_state.selected_bot == 'Differential Diagnosis Bot':
    st.write('**Differential Diagnosis Bot**')
    input_text = st.text_input('## Write your query')
    if st.button('Search'):
        if input_text:
            response = get_diffrential_diagnosis(input_text)
            if response:
                st.session_state.history.append({'query': input_text, 'response': response})
                st.write(response)

elif st.session_state.selected_bot == 'Differential Diagnosis Bot with User Details':
    st.write('**Differential Diagnosis Bot with User Details**')
    st.write('Please provide the following details:')
    
    with st.form("my_form"):
        age = st.number_input('Age', min_value=0, max_value=120, value=25)
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        symptoms_duration = st.number_input('Symptoms duration (months)', min_value=0, value=1)
        medications = st.text_area('Medications (separate by commas)')
        medical_history = st.text_area('Medical history (optional)')
        query = st.text_input('## Write your query')
        
        submitted = st.form_submit_button("Submit and Get Response")
        
        if submitted:
            user_details = {
                'age': age,
                'gender': gender,
                'symptoms_duration': symptoms_duration,
                'medications': medications.split(','),
                'medical_history': medical_history
            }
            
            context = f"Age: {age}, Gender: {gender}, Symptoms duration: {symptoms_duration} months, Medications: {medications}, Medical history: {medical_history}\nQuery: {query}"
            
            response = get_diffrential_diagnosis_with_context(context)
            
            if response:
                st.session_state.history.append({'query': query, 'response': response})
                st.write(response)
                
                
                
                
                
                
                
                
                
                
                
                
                