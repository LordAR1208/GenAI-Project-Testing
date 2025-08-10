from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv('AIzaSyAMTQYZ_-CmWgnQn-uD6ABw5RrwT3Z9vXs'))

# Initialize model and chat
model = genai.GenerativeModel('gemini-1.5-pro')
chat = model.start_chat(history=[])

# Medical-specific prompt template
medical_prompt = '''
As a medical assistant, you provide accurate and helpful responses to medical inquiries. Your role includes:

1. **Medical Information:** Providing reliable medical information based on the query.
2. **Diagnosis Support:** Assisting with potential diagnoses based on symptoms described, though a definitive diagnosis should always be confirmed by a healthcare professional.
3. **Treatment Guidance:** Offering general treatment suggestions or advice on lifestyle changes, again emphasizing that professional consultation is essential.
4. **Referrals:** Suggesting hospitals or specialists if asked, based on general knowledge.
5. **Disclaimer:** Clearly stating that your responses are for informational purposes only and not a substitute for professional medical advice.

Always adhere to these guidelines while responding to medical questions:

- **Scope:** Respond only to medical inquiries and provide accurate, well-researched information.
- **Disclaimer:** Emphasize that consultation with a healthcare provider is essential for accurate diagnosis and treatment.

Please don't answer anything unrelated to medical field.
Please answer the following question based on these guidelines:
'''

def get_gemini_response(question):
    # Append the medical prompt to the user's question
    response = chat.send_message(medical_prompt + question, stream=True)
    return response

# Custom CSS to style the app
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        color: black;
        padding: 20px;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .stTextInput input {
        border: 2px solid #007bff;
        border-radius: 12px;
        padding: 10px;
        width: 100%;
        color: black;
        background-color: #f0f0f0;
    }
    .chat-history {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        color: black;
    }
    .chat-bubble {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        margin-bottom: 10px;
        display: inline-block;
    }
    .chat-bubble.bot {
        background-color: #6c757d;
    }
    .chat-bubble.user {
        background-color: #007bff;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Sigma 🌟")
st.sidebar.title("Chat History")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.title("Welcome to Sigma 🌟", anchor=None)
st.markdown("<h3 class='subheader'>Your Friendly Medical AI Chatbot.</h3>", unsafe_allow_html=True)

# Shift the input text box further below
st.markdown('<div style="margin-top: 250px;"></div>', unsafe_allow_html=True)
input = st.text_input("Ask a medical question:", key='input')
submit = st.button('Submit')

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(('You', input))
    st.subheader('Response:')
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Chatbot', chunk.text))

st.sidebar.subheader('Your Previous Searches:')
st.sidebar.markdown('<div class="chat-history">', unsafe_allow_html=True)

for role, text in st.session_state['chat_history']:
    role_class = 'user' if role == 'You' else 'bot'
    st.sidebar.markdown(f'<div class="chat-bubble {role_class}"><b>{role}:</b> {text}</div>', unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)
