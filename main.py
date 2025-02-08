import streamlit as st
import random
import csv

# Function to load words from CSV file
def load_words_from_csv(filename):
    words = {}
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            words[row["Dutch"]] = row["English"]
    return words

# Load words from CSV
dutch_words = load_words_from_csv("dutch_words.csv")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "word" not in st.session_state:
    st.session_state.word = None
if "options" not in st.session_state:
    st.session_state.options = []
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None

# Function to generate a new question
def new_question():
    word = random.choice(list(dutch_words.keys()))
    correct_translation = dutch_words[word]
    
    # Ensure incorrect choices do not include the correct answer
    incorrect_choices = random.sample(
        [value for value in dutch_words.values() if value != correct_translation], 
        min(3, len(dutch_words) - 1)  # Avoid ValueError if fewer than 4 words exist
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

# Multiple-choice options
choice = st.radio("Select the correct translation:", st.session_state.options)

# Submit button
if st.button("Submit"):
    if choice == st.session_state.correct_answer:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. The correct answer is: **{st.session_state.correct_answer}**")
    
    # Generate a new question and refresh UI
    new_question()
    st.rerun()

# Display Score
st.metric(label="Your Score", value=st.session_state.score)

# Reset Score Button
if st.button("Reset Score"):
    st.session_state.score = 0
    new_question()
    st.rerun()
