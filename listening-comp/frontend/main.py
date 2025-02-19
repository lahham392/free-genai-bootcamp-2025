import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.question_generator import QuestionGenerator

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

def render_header():
    """Render the header section"""
    st.title("&#127466;&#127480; Spanish Interactive Learning")
    st.markdown("""
    Practice Spanish through interactive exercises and get instant feedback.
    Choose from different types of exercises and difficulty levels to improve your Spanish skills.
    """)

def render_interactive_stage():
    """Render the interactive learning stage with RAG-based question generation"""
    st.header("Interactive Learning")
    
    # Initialize session state for question data
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    
    # Practice type and difficulty selection
    col1, col2 = st.columns([2, 1])
    with col1:
        practice_type = st.selectbox(
            "Select Practice Type",
            ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"]
        )
    with col2:
        difficulty = st.selectbox(
            "Select Difficulty",
            ["easy", "medium", "hard"]
        )
    
    # Generate new question button
    if st.button("Generate New Question"):
        with st.spinner("Generating question..."):
            generator = QuestionGenerator()
            question_data = generator.generate_question(practice_type, difficulty)
            if question_data:
                st.session_state.current_question = question_data
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
            st.markdown(f"""**Context:**
            {question_data['context']}
            
            **Question:**
            {question_data['question']}
            """)
            
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
                    st.session_state.feedback = {
                        'is_correct': is_correct,
                        'selected': selected_letter,
                        'detailed': detailed_feedback,
                        'option_feedback': question_data['feedback']
                    }
        
        with col2:
            if practice_type == "Listening Exercise":
                st.subheader("Audio")
                # TODO: Implement audio generation with Amazon Polly
                st.info("Audio feature coming soon!")
            
            # Display feedback if available
            if st.session_state.feedback:
                st.subheader("Feedback")
                if st.session_state.feedback['is_correct']:
                    st.success("¡Correcto! (Correct!)")
                else:
                    st.error(f"Not quite. The correct answer was {question_data['correct_answer']}.")
                
                # Show feedback for selected option
                selected = st.session_state.feedback['selected']
                st.markdown(f"**Your answer ({selected}):**")
                st.write(st.session_state.feedback['option_feedback'][selected])
                
                # Show detailed feedback
                st.markdown("**Detailed Feedback:**")
                st.write(st.session_state.feedback['detailed'])

def main():
    """Main application entry point"""
    render_header()
    render_interactive_stage()

if __name__ == "__main__":
    main()