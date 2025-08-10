import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Define the prompt
prompt = '''
You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:
'''

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('=')[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ''
        for item in transcript_data:
            transcript += ' ' + item['text']
        return transcript

    except Exception as e:
        raise e
    
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        raise e
    
# Streamlit app
st.title('Recapify 📄✨')
st.markdown("<h3 class='subheader'>Your Friendly AI YouTube Summarizer.</h3>", unsafe_allow_html=True)
youtube_link = st.text_input('Enter YouTube video link:')

if youtube_link:
    video_id = youtube_link.split('=')[1]
    st.image(f'http://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)

if st.button('Get Detailed Notes'):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown('## Detailed Notes:')
        st.write(summary)
