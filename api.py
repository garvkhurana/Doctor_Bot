import streamlit as st
import requests

st.title("Doctor Bot")


if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_bot' not in st.session_state:
    st.session_state.selected_bot = 'Query Bot'


with st.sidebar:
    st.write('**Select Bot:**')
    bot_options = ['Query Bot', 'Differential Diagnosis Bot']
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

def get_diffrential_diagnosis(input_text):
    try:
        response = requests.post('http://localhost:8000/diffrential_diagnosis/invoke',
                                 json={'input': {'question': input_text}})
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


input_text = st.text_input('## Write your query')

if st.button('Search'):
    if input_text:
        if st.session_state.selected_bot == 'Query Bot':
            response = get_query_response(input_text)
        else:
            response = get_diffrential_diagnosis(input_text)
        if response:
            st.session_state.history.append({'query': input_text, 'response': response})
            st.write(response)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            