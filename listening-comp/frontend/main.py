import streamlit as st
from typing import Dict
import json
from collections import Counter
import re

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.chat import BedrockChat
from backend.get_transcript import YouTubeTranscriptDownloader
from backend.question_generator import QuestionGenerator


# Page config
st.set_page_config(
    page_title="Spanish Learning Assistant",
    page_icon="\U0001f1ea\U0001f1f8",
    layout="wide"
)   

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

def render_header():
    """Render the header section"""
    st.title("&#127466;&#127480; Spanish Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive Spanish learning experiences.
    
    This tool demonstrates:
    - Base LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - Amazon Bedrock Integration
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with Nova",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with Nova": """
            **Current Focus:**
            - Basic Spanish learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "4. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with Nova")

    # Initialize BedrockChat instance if not in session state
    if 'bedrock_chat' not in st.session_state:
        st.session_state.bedrock_chat = BedrockChat()

    # Introduction text
    st.markdown("""
    Start by exploring Nova's base Spanish language capabilities. Try asking questions about Spanish grammar, 
    vocabulary, or cultural aspects.
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about Spanish language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Spanish?",
            "Explain the difference between は and が",
            "What's the polite form of 食べる?",
            "How do I count objects in Spanish?",
            "What's the difference between こんにちは and こんばんは?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.bedrock_chat.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})



def count_characters(text):
    """Count Spanish and total characters in text"""
    if not text:
        return 0, 0
        
    def is_Spanish(char):
        return any([
            '\u4e00' <= char <= '\u9fff',  # Kanji
            '\u3040' <= char <= '\u309f',  # Hiragana
            '\u30a0' <= char <= '\u30ff',  # Katakana
        ])
    
    jp_chars = sum(1 for char in text if is_Spanish(char))
    return jp_chars, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Spanish lesson YouTube URL"
    )
    
    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                downloader = YouTubeTranscriptDownloader()
                transcript = downloader.get_transcript(url)
                if transcript:
                    # Store the raw transcript text in session state
                    transcript_text = "\n".join([entry['text'] for entry in transcript])
                    st.session_state.transcript = transcript_text
                    st.success("Transcript downloaded successfully!")
                else:
                    st.error("No transcript found for this video.")
            except Exception as e:
                st.error(f"Error downloading transcript: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Raw text",
                value=st.session_state.transcript,
                height=400,
                disabled=True
            )
    
        else:
            st.info("No transcript loaded yet")
    
    with col2:
        st.subheader("Transcript Stats")
        if st.session_state.transcript:
            # Calculate stats
            jp_chars, total_chars = count_characters(st.session_state.transcript)
            total_lines = len(st.session_state.transcript.split('\n'))
            
            # Display stats
            st.metric("Total Characters", total_chars)
            st.metric("Spanish Characters", jp_chars)
            st.metric("Total Lines", total_lines)
        else:
            st.info("Load a transcript to see statistics")

def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dialogue Extraction")
        # Placeholder for dialogue processing
        st.info("Dialogue extraction will be implemented here")
        
    with col2:
        st.subheader("Data Structure")
        # Placeholder for structured data view
        st.info("Structured data view will be implemented here")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")
    
    # Query input
    query = st.text_input(
        "Test Query",
        placeholder="Enter a question about Spanish..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retrieved Context")
        # Placeholder for retrieved contexts
        st.info("Retrieved contexts will appear here")
        
    with col2:
        st.subheader("Generated Response")
        # Placeholder for LLM response
        st.info("Generated response will appear here")

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
    render_header()
    selected_stage = render_sidebar()
    
    # Render appropriate stage
    if selected_stage == "1. Chat with Nova":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "5. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()