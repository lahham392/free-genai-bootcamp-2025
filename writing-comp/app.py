import streamlit as st

# Set up the Streamlit page - must be the first st command
st.set_page_config(page_title="Spanish Writing Practice", layout="wide")

import os
from streamlit_drawable_canvas import st_canvas
from bedrock_service import BedrockChat
from ocr_service import HandwritingRecognizer
from utils import TOPICS, DIFFICULTIES, FALLBACK_SENTENCES

# Initialize services
@st.cache_resource
def init_services():
    return BedrockChat(), HandwritingRecognizer()

bedrock_chat, handwriting_recognizer = init_services()

st.title("Spanish Writing Practice")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    selected_topic = st.selectbox("Select Topic", list(TOPICS.keys()))
    difficulty = st.selectbox("Select Difficulty", DIFFICULTIES)

# Initialize session state
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = None
    st.session_state.complete_sentence = None
    st.session_state.missing_word = None
    st.session_state.show_result = False
    st.session_state.canvas_key = 0

# Generate new sentence button
if st.button("Get New Sentence") or st.session_state.current_sentence is None:
    try:
        incomplete, complete, missing = bedrock_chat.generate_spanish_sentence(selected_topic, difficulty)
        if incomplete and complete and missing:
            st.session_state.current_sentence = incomplete
            st.session_state.complete_sentence = complete
            st.session_state.missing_word = missing.lower()
        else:
            # Use fallback sentences if AWS Bedrock fails
            incomplete, complete, missing = FALLBACK_SENTENCES[selected_topic][difficulty]
            st.session_state.current_sentence = incomplete
            st.session_state.complete_sentence = complete
            st.session_state.missing_word = missing.lower()
    except Exception as e:
        st.error(f"Error generating sentence. Using fallback sentence.")
        incomplete, complete, missing = FALLBACK_SENTENCES[selected_topic][difficulty]
        st.session_state.current_sentence = incomplete
        st.session_state.complete_sentence = complete
        st.session_state.missing_word = missing.lower()
    
    st.session_state.show_result = False
    st.session_state.canvas_key += 1

# Display the current sentence
if st.session_state.current_sentence:
    st.header("Complete the Sentence")
    st.write(st.session_state.current_sentence)

    # Create drawing canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Color for fill
        stroke_width=2,  # Width of stroke
        stroke_color="#000000",  # Color of stroke
        background_color="#eee",  # Canvas background
        height=150,  # Canvas height
        width=400,  # Canvas width
        drawing_mode="freedraw",  # Drawing mode
        key=f"canvas_{st.session_state.canvas_key}",  # Unique key for canvas
        display_toolbar=True,  # Display toolbar with options
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Submit"):
            if canvas_result.image_data is not None:
                with st.spinner("Recognizing handwriting..."):
                    # Get the recognized text
                    recognized_text = handwriting_recognizer.recognize_text(canvas_result.image_data)
                    
                    if recognized_text:
                        st.session_state.show_result = True
                        
                        # Compare with correct answer
                        if recognized_text.lower() == st.session_state.missing_word.lower():
                            st.success(f"¡Correcto! You wrote: {recognized_text}")
                        else:
                            st.error(f"Not quite. You wrote: {recognized_text}")
                            
                        st.write(f"Correct word was: {st.session_state.missing_word}")
                        st.write(f"Complete sentence: {st.session_state.complete_sentence}")
                    else:
                        st.error("Could not recognize the handwriting. Please try again.")
    
    with col2:
        if st.button("Clear Drawing"):
            st.session_state.canvas_key += 1  # This will force a new canvas
            st.experimental_rerun()
