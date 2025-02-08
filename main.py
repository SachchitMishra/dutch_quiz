import streamlit as st
import random

# Dictionary of Dutch words and their English meanings
dutch_words = {
    "ik": "I", "je": "you (informal)", "het": "it", "de": "the", "dat": "that",
    "is": "is", "een": "a, one", "niet": "not", "en": "and", "wat": "what",
    "van": "of, from", "we": "we", "in": "in", "ze": "they, she", "hij": "he",
    "op": "on", "te": "to, too", "zijn": "to be, his, their", "er": "there",
    "maar": "but", "die": "that, those", "heb": "have (I form)", "me": "me",
    "met": "with", "voor": "for", "als": "if, as", "ben": "am", "was": "was",
    "dit": "this", "mijn": "my", "om": "around, for", "aan": "on, at, to",
    "jij": "you (emphatic)", "naar": "to, towards", "dan": "than, then",
    "hier": "here", "weet": "know (I/he/she/it form)", "kan": "can", "geen": "no, none",
    "nog": "still, yet", "moet": "must, have to", "wil": "want", "wel": "indeed, surely",
    "ja": "yes", "zo": "so, like that", "heeft": "has", "hebben": "to have",
    "hem": "him", "goed": "good", "nee": "no", "waar": "where, true",
    "nu": "now", "hoe": "how", "ga": "go (I form)", "haar": "her, hair",
    "uit": "out", "doen": "to do", "ook": "also, too", "over": "about, over",
    "bent": "are (you form)", "mij": "me", "gaan": "to go", "of": "or",
    "kom": "come (I form)", "zou": "would", "al": "already, all", "bij": "at, near",
    "daar": "there", "ons": "us, our", "jullie": "you (plural)", "hebt": "have (you form)"
}

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "word" not in st.session_state:
    st.session_state.word = None
if "options" not in st.session_state:
    st.session_state.options = []

# Function to generate new question
def new_question():
    word = random.choice(list(dutch_words.keys()))
    correct_translation = dutch_words[word]
    
    # Get three incorrect choices
    incorrect_choices = random.sample(list(dutch_words.values()), 3)
    
    # Ensure correct translation is not duplicated
    while correct_translation in incorrect_choices:
        incorrect_choices = random.sample(list(dutch_words.values()), 3)
    
    # Create choices list and shuffle
    choices = incorrect_choices + [correct_translation]
    random.shuffle(choices)

    # Store in session state
    st.session_state.word = word
    st.session_state.options = choices
    st.session_state.correct_answer = correct_translation

# Generate first question if not set
if not st.session_state.word:
    new_question()

# App Title
st.title("Dutch to English Translation Quiz")

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
    
    # Generate new question
    new_question()

# Display Score
st.write(f"**Score: {st.session_state.score}**")

# Reset Score Button
if st.button("Reset Score"):
    st.session_state.score = 0
    new_question()
    st.experimental_rerun()