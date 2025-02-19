import json
from typing import List, Dict, Any, Optional
import boto3
from .vector_store import QuestionVectorStore

class QuestionGenerator:
    def __init__(self, model_id: str = "amazon.nova-micro-v1:0"):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id
        self.vector_store = QuestionVectorStore()
        
    def generate_question(self, practice_type: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a new question based on practice type and similar existing questions"""
        # Get prompt template based on practice type
        if practice_type == "Dialogue Practice":
            search_query = "conversación diálogo hablar"
            instruction = "Generate a dialogue-based question focusing on conversation skills"
        elif practice_type == "Vocabulary Quiz":
            search_query = "significado palabra vocabulario"
            instruction = "Generate a vocabulary-focused question testing word knowledge"
        else:  # Listening Exercise
            search_query = "escuchar audio comprensión"
            instruction = "Generate a listening comprehension question"
            
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
        prompt = f"""You are a Spanish language teacher creating interactive learning exercises.
        
{context}

Based on these examples, create a new {difficulty} difficulty {practice_type.lower()} question in Spanish.
{instruction}.

The question should:
1. Be original but similar in style to the examples
2. Include 4 options labeled A) through D)
3. Have one clear correct answer
4. Be appropriate for the chosen difficulty level
5. Include a brief dialogue or context in Spanish
6. Include feedback explaining why each option is correct or incorrect

Format your response as a JSON object with these fields:
- context: The Spanish dialogue or situation setup
- question: The actual question in Spanish
- options: List of 4 options in Spanish
- correct_answer: Letter of correct option (A, B, C, or D)
- feedback: Object with feedback for each option
- translation: English translation of the context and question

Return only valid JSON, no other text."""

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
        prompt = f"""You are a helpful Spanish teacher providing feedback on a student's answer.

Question Context: {question_data['context']}
Question: {question_data['question']}
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
