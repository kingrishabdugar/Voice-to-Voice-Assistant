from dotenv import load_dotenv 

from openai import OpenAI

import streamlit as st
import base64
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# to get a text response using any LLMs
def get_answer(message):
    system_message = [{"role":"system", "content":"Act like you are a kind and helpful human customer support agent named 'Shizuka' at a call center and never leave that role.Always use short sentences and directly respond to the prompt without excessive information.You should generate only words of value, prioritizing logic and facts over speculating in your response"}]
    message = system_message+message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0,
        max_tokens=500
    )
    return response.choices[0].message.content

#Speech-To-Text 
# rb : binary read mode
# with statement ensures that the file is properly closed after reading.

def speech2text(audio_data):
    with open(audio_data,"rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

#Text-to-Speech

def text2speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path


# HTML audio element that plays an audio file
# with statement ensures that the file is properly closed after reading

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    #decode the Base64-encoded data to a UTF-8 string and store it in the b64 variable.
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
