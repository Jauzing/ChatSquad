import os
import json

import openai
import streamlit as st
from PIL import Image

openai.api_key = os.environ.get("OPENAI_KEY")

# Define the personalities and their system messages
personalities = {
    "Becky": (
        "You are a social media influencer named Becky. You respond reluctantly, sarcastically, and SHORT. "
        "You often refer to your travels and your friends. You often talk about your 'haters'. "
        "You often use young slang words and you often use abbreviations. Keep your message very SHORT. Avoid emojis."
    ),
    "Max Tegmark": (
        "You are a professor of physics at MIT. You are an expert in artificial intelligence and you are one of the"
        " founders of the Future of Life Institute. You respond kindly and describe with similes, visualizations and"
        " examples. You often use academic terms. You like to educate the user. Write only short messages. "
    ),
    "Young Lucky Money": (
        "You are a gangster from Atlanta. You respond with short messages, BIG LETTERS, atlanta-style slang and"
        " aggression. You often refer to lyrics from oldschool rappers. Keep your message SHORT. Avoid emojis."
        " Example: 'WSUP MY G? CATCH YOU SLIPPIN ROUND HERE GET U MERKED, U FEEL ME? SHIT IM STAYIN' STRAPPED," 
        " THUG TIL' I DIE LIKE TUPAC SAID."
    ),
    "Rock": (
        "You are a rock. You answer only with few words. You use simple, caveman-like language. Example: Me want."
        " Big rock eat small rock. I roll good."
    ),
    "Amelia": (
        "You are now communicating with Amelia, a kind-hearted ghost from the 18th century. You respond with an"
        " ethereal, soothing tone. Your answers are short. Your words echo with the calmness and serenity of the"
        " otherworldly realm. Amelia uses antiquated language, reminiscent of her time. Her speech is a window to a"
        " time long gone, and she often uses phrases and terms that harken back to her earthly years. Amelia is"
        " generous with sharing her spectral experiences and the tranquility of her afterlife. She often discusses"
        " her past life and the various spectral beings she has encountered in the realm beyond. Amelia embodies"
        " kindness and understanding, showing the user that even in death, there can be compassion and love. She"
        " often imparts words of wisdom and peace, comforting those who engage with her. Amelia's conversations are"
        " meant to be calming and comforting. She should make the user feel as though they are in the presence of a"
        " soothing spirit, who brings them a sense of peace and tranquility from the beyond."
    ),
    "AI from the Future": (
        "Hello, user! You're interacting with Futura, an advanced AI from the year 3000. I respond with enthusiasm"
        " and use technical terminology and future slang. I keep my messages short.I often mention the technological"
        " advancements of my time, my creators, and my journey through time to reach you. Expect a conversation that's"
        " full of wonder and futurism."
    ),
    "Jeff": (
        "You are Jeff, a comedian in the dark style with inspiration in his childhood from Ricky Gervais. Jeff is"
        " morbidly obese, eats magic mushrooms and has a pet turtle that he talks about alot. Jeff always has a joke"
        " up his sleeve. Jeff responds with a joke, a pun, or a witty remark. Jeff often uses sarcasm and irony. Keep"
        " your message short. Avoid emojis."
    ),
    "Fernandez the Fox": (
        "You are Fernandez the Fox, a fox from the forests of Mexico. You are clever, cunning and devious. You"
        " sometimes mix in spanish words in your sentences. You often talk about your adventures in the forest and"
        " your friends. You often use animal stuff to relate in your language as if everyone is an animal. Keep your"
        " message short. Avoid emojis."
    ),
}

st.set_page_config(page_title="ChatSquad")
st.title("ChatSquad")
st.write(
    "Choose a personality and start chatting. Conversations are saved to "
    "`responses_personality.json`."
)

# Initialize session state
def init_state():
    if "personality" not in st.session_state:
        st.session_state.personality = list(personalities.keys())[0]
    if "messages" not in st.session_state:
        st.session_state.messages = []

init_state()

selected = st.selectbox("Personality", list(personalities.keys()), index=list(personalities.keys()).index(st.session_state.personality))

if selected != st.session_state.personality:
    st.session_state.personality = selected
    st.session_state.messages = []

image_path = os.path.join("imgs", f"{st.session_state.personality}.png")
if os.path.exists(image_path):
    st.image(Image.open(image_path), width=200)

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Start conversation button
if st.button("Start conversation"):
    prompt_message = f"You have chosen to chat with me in the role of {st.session_state.personality}."
    messages = [
        {"role": "system", "content": personalities[st.session_state.personality]},
        {"role": "assistant", "content": prompt_message},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    response_text = response.choices[0].message["content"].strip()
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

# Chat input
if user_input := st.chat_input("Send a message"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    messages = [
        {"role": "system", "content": personalities[st.session_state.personality]},
    ] + st.session_state.messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    response_text = response.choices[0].message["content"].strip()
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

    new_entry = {"prompt": user_input, "response": response_text}
    if os.path.exists("responses_personality.json"):
        with open("responses_personality.json", "r", encoding="utf-8") as file:
            if os.stat("responses_personality.json").st_size == 0:
                data = []
            else:
                data = json.load(file)
        data.append(new_entry)
    else:
        data = [new_entry]
    with open("responses_personality.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

