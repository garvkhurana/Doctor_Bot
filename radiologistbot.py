import streamlit as st
import base64
import os
from langchain_community.llms import Ollama
import tempfile


llm = Ollama(model="llava:34b")

sample_prompt =""" You are a board-certified radiologist with expertise in interpreting medical images. Analyze the provided image and provide a detailed report, including:
Image type (e.g., X-ray, CT, MRI etc)
Body part/region imaged
Any visible abnormalities or findings
Potential diagnoses or differential diagnoses
"""

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'result' not in st.session_state:
    st.session_state.result = None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def call_ollama_model_for_analysis(filename: str, sample_prompt=sample_prompt):
    base64_image = encode_image(filename)
    
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": sample_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }
    ]

    prompt = messages[0]["content"][0]["text"]
    response = llm(prompt)
    formatted_response = f"Findings:\n\n{response}\n\nDisclaimer: Consult with a Doctor before making any decisions."
    return formatted_response
    
st.title("Medical Help using Multimodal LLM")


uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])  


if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        st.session_state['filename'] = tmp_file.name

    st.image(uploaded_file, caption='Uploaded Image')

if st.button('Analyze Image'):
    if 'filename' in st.session_state and os.path.exists(st.session_state['filename']):
        try:
            st.session_state['result'] = call_ollama_model_for_analysis(st.session_state['filename'])
            st.text_area("", value=st.session_state['result'], height=300)
        finally:
            os.unlink(st.session_state['filename'])
            
            
            
            
            
            
            