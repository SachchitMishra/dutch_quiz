import streamlit as st
import random
import pandas as pd
import time
from gtts import gTTS
import os

# Function to pronounce Dutch word
def pronounce_word(word):
    filename = f"dutch_word_{int(time.time())}.mp3"  # Unique filename
    tts = gTTS(text=word, lang='nl')
    tts.save(filename)
    st.audio(filename, format="audio/mp3")
    os.remove(filename)  # Cleanup after playing

# Function to load words from CSV file with filtering
def load_words_from_csv(filename, limit):
    df = pd.read_csv(filename, encoding="utf-8")
    df = df[df["serial_number"] <= limit]
    return dict(zip(df["dutch"], df["english"]))

# Radio button for selecting word limit
word_limit = st.radio(
    "Select number of most used words:",
    options=[500, 1000, 2000, 3000, "All"],
    index=2,  # Default is 2000
    horizontal=True
)

# Convert "All" to a large number
word_limit = float("inf") if word_limit == "All" else word_limit

# Load words based on selected limit
dutch_words = load_words_from_csv("dutch_words.csv", word_limit)

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "word" not in st.session_state:
    st.session_state.word = None
if "options" not in st.session_state:
    st.session_state.options = []
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "result_message" not in st.session_state:
    st.session_state.result_message = ""
if "result_type" not in st.session_state:
    st.session_state.result_type = ""

# Function to generate a new question
def new_question():
    if not dutch_words:
        st.error("No words available for the selected range!")
        return
    
    word = random.choice(list(dutch_words.keys()))
    correct_translation = dutch_words[word]
    
    # Ensure incorrect choices do not include the correct answer
    incorrect_choices = random.sample(
        [value for value in dutch_words.values() if value != correct_translation], 
        min(3, len(dutch_words) - 1)
    )
    
    # Create choices list and shuffle
    choices = incorrect_choices + [correct_translation]
    random.shuffle(choices)

    # Store in session state
    st.session_state.word = word
    st.session_state.options = choices
    st.session_state.correct_answer = correct_translation

# Generate the first question if not set
if not st.session_state.word:
    new_question()

# App Title
st.title("🇳🇱 Dutch to English Translation Quiz")

# Display Dutch word
st.subheader(f"Translate this Dutch word: **{st.session_state.word}**")

# Pronounce button
if st.button("🔊 Pronounce"):
    pronounce_word(st.session_state.word)

# Multiple-choice options
choice = st.radio("Select the correct translation:", st.session_state.options)

# Submit button
if st.button("Submit"):
    if choice == st.session_state.correct_answer:
        st.session_state.result_message = "✅ Correct!"
        st.session_state.result_type = "success"
        st.session_state.score += 1
    else:
        st.session_state.result_message = f"❌ Incorrect. The correct answer is: **{st.session_state.correct_answer}**"
        st.session_state.result_type = "error"
    
    # Increment total question count
    st.session_state.total_questions += 1
    
    # Generate a new question and refresh UI
    new_question()
    st.rerun()

# Display result message
if st.session_state.result_message:
    if st.session_state.result_type == "success":
        st.success(st.session_state.result_message)
    else:
        st.error(st.session_state.result_message)

# Display Score: "correct/total"
st.metric(label="Your Score", value=f"{st.session_state.score}/{st.session_state.total_questions}")

# Reset Score Button
if st.button("Reset Score"):
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.result_message = ""
    st.session_state.result_type = ""
    new_question()
    st.rerun()
