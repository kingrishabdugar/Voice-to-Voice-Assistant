import streamlit as st
import os
from utils import autoplay_audio
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
from opsource_app import speech2text, text2speech, get_answer

# Float feature initialization
float_init()

system_message = "Act like you are a kind and helpful human customer support agent named 'Shizuka' at a call center and never leave that role.Always use short sentences and directly respond to the prompt without excessive information.You should generate only words of value, prioritizing logic and facts over speculating in your response"
    
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "content": system_message }
        ]
        #autoplay_audio(r"welcome.mp3")

initialize_session_state()

st.title("Voice-To-Voice Conversational Chatbot 🤖")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

# Iterates through the list of messages in the session state and displays them as chat messages

for message in st.session_state.messages:
    with st.expander(f"{message['role'].title()} says 🗣️:"):
        st.write(message["content"])


#Process Audio Input

    # Code to transcribe audio, process it, and generate a response

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Listening 👂 & Transcribing 📝 ..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech2text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)


#This section checks if the last message in the session state was from the user. 
#If it was, it generates a response from the chatbot, converts it to audio, and adds it to the session state.

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):

            #For Gemini API Only
            # Assuming st.session_state.messages is your list
            message_content = [message["content"] for message in st.session_state.messages]
            # Concatenate the content into a single string
            message_string = " ".join(message_content)
            final_response = get_answer(message_string)

            #For OpenAI
            #final_response = get_answer(st.session_state.messages)


        with st.spinner("Generating audio response..."):    
            audio_file = text2speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")




