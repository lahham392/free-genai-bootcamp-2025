import streamlit as st
import sys
import os
import json
from datetime import datetime
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.question_generator import QuestionGenerator
from backend.audio_generator import AudioGenerator

# Create static directory for audio files
static_dir = Path(__file__).parent / "static" / "audio_cache"
static_dir.mkdir(parents=True, exist_ok=True)

# Constants
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'question_history.json')

def load_question_history():
    """Load question history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading question history: {str(e)}")
            return []
    return []

def save_question_history(history):
    """Save question history to JSON file"""
    try:
        # Add timestamp to each question if not present
        for question in history:
            if 'timestamp' not in question:
                question['timestamp'] = datetime.now().isoformat()
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving question history: {str(e)}")

# Page config
st.set_page_config(
    page_title="Spanish Interactive Learning",
    page_icon="\U0001f1ea\U0001f1f8",
    layout="wide"
)

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'question_history' not in st.session_state:
    st.session_state.question_history = load_question_history()
if 'audio_path' not in st.session_state:
    st.session_state.audio_path = None

def render_header():
    """Render the header section"""
    st.title("&#127466;&#127480; Spanish Interactive Learning")
    st.markdown("""
    Practice Spanish through interactive exercises and get instant feedback.
    Choose from different types of exercises and difficulty levels to improve your Spanish skills.
    """)

def render_sidebar():
    """Render the sidebar with question history"""
    with st.sidebar:
        st.header("Question History")
        if not st.session_state.question_history:
            st.info("No questions generated yet")
        else:
            st.write(f"Total questions: {len(st.session_state.question_history)}")
            
            # Sort questions by timestamp (newest first)
            sorted_questions = sorted(
                st.session_state.question_history,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )
            
            # Add a clear history button
            if st.button("Clear History", type="secondary"):
                st.session_state.question_history = []
                save_question_history([])
                st.rerun()
            
            # Display questions with timestamps
            for idx, q in enumerate(sorted_questions):
                timestamp = datetime.fromisoformat(q.get('timestamp', '')).strftime('%Y-%m-%d %H:%M')
                if st.button(f"[{timestamp}] Question {idx + 1}: {q['question'][:50]}...", key=f"q_{idx}"):
                    st.session_state.current_question = q
                    st.session_state.feedback = None
                    st.rerun()

def render_interactive_stage():
    """Render the interactive learning stage with RAG-based question generation"""
    st.header("Interactive Learning")
    
    # Practice type, topic and difficulty selection
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        practice_type = st.selectbox(
            "Select Practice Type",
            ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"]
        )
    with col2:
        topic = st.selectbox(
            "Select Topic",
            [
                "Restaurant and Food",
                "Shopping and Retail",
                "Travel and Transportation",
                "Work and Business",
                "Family and Relationships",
                "Health and Medical",
                "Education and Learning",
                "Entertainment and Leisure",
                "Home and Daily Life",
                "Weather and Seasons"
            ]
        )
    with col3:
        difficulty = st.selectbox(
            "Select Difficulty",
            ["easy", "medium", "hard"]
        )
    
    # Generate new question button
    if st.button("Generate New Question"):
        with st.spinner("Generating question..."):
            generator = QuestionGenerator()
            question_data = generator.generate_question(practice_type, difficulty, topic)
            if question_data:
                st.session_state.current_question = question_data
                # Add to question history if it's not already there
                if question_data not in st.session_state.question_history:
                    question_data['timestamp'] = datetime.now().isoformat()
                    st.session_state.question_history.append(question_data)
                    # Save to file
                    save_question_history(st.session_state.question_history)
                st.session_state.feedback = None
            else:
                st.error("Failed to generate question. Please try again.")
                return
    
    # Display current question if available
    if not st.session_state.current_question:
        st.info("Click 'Generate New Question' to start practicing!")
    else:
        question_data = st.session_state.current_question
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Practice Scenario")
            # Display context and question
            # Display Introduction
            st.markdown("**Introduction:**")
            st.write(question_data['introduction'])
            
            # Display Conversation
            st.markdown("**Conversation:**")
            st.write(question_data['conversation'])
            
            # Display Question
            st.markdown("**Question:**")
            st.write(question_data['question'])
            
            # Display translation in expandable section
            with st.expander("Show English Translation"):
                st.write(question_data['translation'])
            
            # Multiple choice options
            options = [opt.strip() for opt in question_data['options']]
            selected = st.radio("Choose your answer:", options)
            
            # Submit answer button
            if st.button("Submit Answer"):
                selected_letter = chr(65 + options.index(selected))  # Convert to A, B, C, D
                is_correct = selected_letter == question_data['correct_answer']
                
                # Get detailed feedback
                with st.spinner("Generating feedback..."):
                    generator = QuestionGenerator()
                    detailed_feedback = generator.get_additional_feedback(
                        question_data,
                        selected
                    )
                    feedback_data = {
                        'is_correct': is_correct,
                        'selected': selected_letter,
                        'detailed': detailed_feedback,
                    }
                    
                    # Add option-specific feedback if available
                    if 'feedback' in question_data:
                        feedback_data['option_feedback'] = question_data['feedback']
                    else:
                        feedback_data['option_feedback'] = None
                        
                    st.session_state.feedback = feedback_data
        
        with col2:
            # Audio section for all question types
            st.subheader("Audio Playback")
            
            # Generate audio button
            if st.button("Generate Audio", key="generate_audio"):
                with st.spinner("Generating audio..."):
                    audio_generator = AudioGenerator()
                    audio_path = audio_generator.generate_audio(question_data)
                    if audio_path:
                        st.session_state.audio_path = audio_path
                        st.success("Audio generated successfully!")
                    else:
                        st.error("Failed to generate audio. Please try again.")
            
            # Display audio player if audio is available
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                st.audio(st.session_state.audio_path)
            elif st.session_state.audio_path:
                st.warning("Audio file not found. Try generating it again.")
            
            # Display feedback if available
            if st.session_state.feedback:
                st.subheader("Feedback")
                if st.session_state.feedback['is_correct']:
                    st.success("¡Correcto! (Correct!)")
                else:
                    st.error(f"Not quite. The correct answer was {question_data['correct_answer']}.")
                
                # Display detailed feedback
                if st.session_state.feedback['detailed']:
                    st.write(st.session_state.feedback['detailed'])
                    
                # Display option-specific feedback if available
                if st.session_state.feedback.get('option_feedback'):
                    st.write("Option-specific feedback:")
                    st.write(st.session_state.feedback['option_feedback'])
                selected = st.session_state.feedback['selected']
                st.markdown(f"**Your answer ({selected}):**")
                st.write(st.session_state.feedback['option_feedback'][selected])
                
                # Show detailed feedback
                st.markdown("**Detailed Feedback:**")
                st.write(st.session_state.feedback['detailed'])

def main():
    """Main application entry point"""
    render_header()
    render_sidebar()
    render_interactive_stage()

if __name__ == "__main__":
    main()