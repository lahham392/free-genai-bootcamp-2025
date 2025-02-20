import json
from typing import List, Dict, Any, Optional
import boto3
from .vector_store import QuestionVectorStore

class QuestionGenerator:
    def __init__(self, model_id: str = "amazon.nova-micro-v1:0"):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id
        self.vector_store = QuestionVectorStore()
        
    def generate_question(self, practice_type: str, difficulty: str = "medium", topic: str = "General") -> Dict[str, Any]:
        """Generate a new question based on practice type, topic and similar existing questions"""
        # Get prompt template based on practice type and topic
        if practice_type == "Dialogue Practice":
            search_query = f"conversación diálogo {topic.lower()}"
            instruction = f"Generate a dialogue-based question about {topic}"
        elif practice_type == "Vocabulary Quiz":
            search_query = f"vocabulario {topic.lower()}"
            instruction = f"Generate a vocabulary-focused question about {topic}"
        else:  # Listening Exercise
            search_query = f"escuchar comprensión {topic.lower()}"
            instruction = f"Generate a listening comprehension question about {topic}"
            
        # Get similar questions for context
        similar_questions = self.vector_store.search_similar_questions(search_query, n_results=3)
        
        # Format context from similar questions
        context = "Here are some example Spanish learning questions:\n\n"
        for i, q in enumerate(similar_questions, 1):
            context += f"Example {i}:\n"
            context += f"Question: {q['text']}\n"
            context += f"Options: {q['metadata']['options']}\n"
            context += f"Correct Answer: {q['metadata']['correct_answer']}\n\n"
        
        # Create the prompt
        prompt = f"""Create a Spanish language learning exercise about {topic} following this EXACT format:

Introduction:
[A brief setting description with 2-3 people in a {topic}-related situation]

Conversation:
[Natural dialogue between the people, with clear speaker labels, containing a piece of information that will be asked about]

Question:
[A question about specific information from the dialogue]
A) [option]
B) [option]
C) [option]
D) [option]

Example format:
Introduction:
Un cliente y un camarero están hablando en un restaurante

Conversation:
Cliente: ¿Cuál es el especial del día?
Camarero: Hoy tenemos paella de mariscos por 15 euros.
Cliente: ¿Y viene con alguna bebida?
Camarero: Sí, incluye una copa de vino blanco o tinto.
Cliente: Perfecto, tomaré la paella con vino tinto.

Question:
¿Qué bebida elige el cliente?
A) vino blanco
B) vino tinto
C) agua mineral
D) cerveza

Create a new {difficulty} difficulty dialogue in Spanish about {topic} following this EXACT structure. The dialogue should:
1. Be in Spanish
2. Have 2-3 speakers in a realistic {topic}-related situation
3. Include a clear piece of information that will be asked about
4. Have 4 clear answer options
5. Match the {difficulty} difficulty level:
   - Easy: Basic greetings, simple present tense
   - Medium: Past tense, opinions, feelings
   - Hard: Complex situations, subjunctive, idiomatic expressions

Format your response as a JSON object with these fields:
- introduction: The introduction text in Spanish
- conversation: The conversation text in Spanish with speaker labels
- question: The question text in Spanish
- options: Array of 4 options in Spanish [A, B, C, D]
- correct_answer: Letter of correct option (A, B, C, or D)
- translation: English translation of everything

Return only valid JSON."""

        # Call Bedrock
        try:
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]
            
            inference_config = {
                "temperature": 0.7,
                "maxTokens": 1000
            }
            
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            response_text = response['output']['message']['content'][0]['text']
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            return None
            
    def get_additional_feedback(self, question_data: Dict[str, Any], user_answer: str) -> str:
        """Get detailed feedback for user's answer using Claude"""
        # Build context section based on available data
        context_section = ""
        if 'context' in question_data:
            context_section = f"Question Context: {question_data['context']}\n"
        elif 'dialogue' in question_data:
            context_section = f"Dialogue Context: {question_data['dialogue']}\n"

        prompt = f"""You are a helpful Spanish teacher providing feedback on a student's answer.

{context_section}Question: {question_data['question']}
Student's Answer: {user_answer}
Correct Answer: {question_data['correct_answer']}

Provide encouraging and educational feedback in English that:
1. Explains why the answer is correct or incorrect
2. Provides relevant grammar or vocabulary tips
3. Suggests a learning strategy or mnemonic device if applicable
4. Maintains a positive and supportive tone

Keep the feedback concise but helpful."""

        try:
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]
            
            inference_config = {
                "temperature": 0.7,
                "maxTokens": 300
            }
            
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            return response['output']['message']['content'][0]['text']
            
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return "Sorry, I couldn't generate detailed feedback at this time."
