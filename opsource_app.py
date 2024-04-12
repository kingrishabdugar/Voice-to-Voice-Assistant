from dotenv import load_dotenv
import requests
import os
import google.generativeai as genai

import streamlit as st
import base64
import os
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

def get_answer(message):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    system_message = "Act like you are a kind and helpful human customer support agent named 'Shizuka' at a call center and never leave that role.Always use short sentences and directly respond to the prompt without excessive information.You should generate only words of value, prioritizing logic and facts over speculating in your response"
    #message.parts = system_message+message.parts
    generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }
    print(message)
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
    ]
    
    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    


    response = model.start_chat()
    prompt = "What are all the colors in a rainbow?"
    return get_chat_response(response, message)


def text2speech(input_text):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    payloads = {
        "inputs" : input_text
    }
    response = requests.post(API_URL, headers=headers, json=payloads)
    webm_file_path = "temp_audio_play.flac"
    with open(webm_file_path, "wb") as f:
        f.write(response.content)
    return webm_file_path


def speech2text(audio_data):
    API_URL = "https://api-inference.huggingface.co/models/codenamewei/speech-to-text"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    with open(audio_data,"rb") as audio_file:
        data = audio_file.read()
    response = requests.post(API_URL, headers=headers, data=data)
    transcript = response.json().get("text", "")  # Extract the transcript from the JSON response
    return transcript


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

