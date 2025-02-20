import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
import json
import boto3
import numpy as np
from pathlib import Path

class BedrockEmbeddings:
    """Wrapper for Bedrock's embedding models"""
    EMBEDDING_DIMENSION = 1024  # Titan model's embedding dimension
    def __init__(self, model_id: str = "amazon.titan-embed-text-v2:0"):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id

    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Bedrock's Titan model"""
        embeddings = []
        for text in input:
            try:
                body = json.dumps({"inputText": text})
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=body
                )
                response_body = json.loads(response['body'].read())
                embedding = response_body['embedding']
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error generating embedding: {str(e)}")
                # Return a zero vector as fallback
                embeddings.append([0.0] * self.EMBEDDING_DIMENSION)
        return embeddings

class QuestionVectorStore:
    def __init__(self, persist_directory: str = "question_db", recreate: bool = False):
        """Initialize the vector store for questions with Bedrock embeddings"""
        self.persist_directory = persist_directory
        self.embeddings = BedrockEmbeddings()
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            is_persistent=True
        ))
        
        # Delete existing collection if recreate is True
        if recreate:
            try:
                self.client.delete_collection("spanish_questions")
                print("Deleted existing collection")
            except ValueError:
                pass  # Collection doesn't exist
        
        # Get existing collection or create new one
        try:
            self.collection = self.client.get_collection(
                name="spanish_questions",
                embedding_function=self.embeddings
            )
        except (ValueError, chromadb.errors.InvalidCollectionException):
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(
                name="spanish_questions",
                metadata={"hnsw:space": "cosine", "dimension": BedrockEmbeddings.EMBEDDING_DIMENSION},
                embedding_function=self.embeddings
            )

    def add_questions(self, questions: List[Dict[str, Any]]):
        """
        Add questions to the vector store
        
        Args:
            questions: List of dictionaries containing:
                - text: The question text
                - scenario_id: ID of the scenario this question belongs to
                - options: List of possible answers
                - correct_answer: The correct answer
        """
        documents = []
        ids = []
        metadatas = []
        
        for i, q in enumerate(questions):
            # Only add questions that have all required fields
            if q["text"] and q["options"] and q["correct_answer"]:
                documents.append(q["text"])
                ids.append(f"q_{i}")
                metadatas.append({
                    "scenario_id": q["scenario_id"],
                    "options": str(q["options"]),
                    "correct_answer": q["correct_answer"],
                    "topic": q["topic"]
                })
        
        if documents:  # Only add if we have valid questions
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )

    def search_similar_questions(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar questions
        
        Args:
            query: The question text to find similar questions for
            n_results: Number of similar questions to return
            
        Returns:
            List of similar questions with their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        similar_questions = []
        for i in range(len(results["documents"][0])):
            similar_questions.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
            
        return similar_questions

    def get_question_by_id(self, question_id: str) -> Dict[str, Any]:
        """Retrieve a specific question by its ID"""
        result = self.collection.get(ids=[question_id])
        if result["documents"]:
            return {
                "text": result["documents"][0],
                "metadata": result["metadatas"][0]
            }
        return None

def parse_structured_file(file_path: str) -> List[Dict[str, Any]]:
    """Parse the structured transcript file into a list of questions"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scenarios = content.split('### Scenario')[1:]  # Split by scenarios, ignore empty first part
    questions = []
    
    for scenario_idx, scenario in enumerate(scenarios, 1):
        try:
            # Extract scenario information
            lines = scenario.strip().split('\n')
            topic = next(line for line in lines if '**Topic:**' in line).split('**Topic:**')[1].strip()
            
            # Find all questions in this scenario
            question_sections = scenario.split('**Question:**')[1:]  # First part is scenario info
            
            for q_section in question_sections:
                try:
                    # Extract question text - everything up to Options or first newline if no Options marker
                    if '**Options:**' in q_section:
                        question_text = q_section.split('**Options:**')[0].strip()
                    else:
                        question_text = q_section.split('\n')[0].strip()
                    
                    # Extract options
                    options = []
                    if '**Options:**' in q_section:
                        options_text = q_section.split('**Options:**')[1]
                        if '**Correct Answer:**' in options_text:
                            options_text = options_text.split('**Correct Answer:**')[0]
                        
                        # Clean up options
                        for line in options_text.strip().split('\n'):
                            line = line.strip()
                            if line and any(line.startswith(p) for p in ['A)', 'B)', 'C)', 'D)']):
                                options.append(line)
                    
                    # Extract correct answer
                    correct_answer = ''
                    if '**Correct Answer:**' in q_section:
                        answer_part = q_section.split('**Correct Answer:**')[1].strip()
                        correct_answer = answer_part.split('\n')[0].strip() or ''  # Empty string if no answer
                    
                    if question_text:  # Only add if we have a question
                        questions.append({
                            'text': question_text,
                            'scenario_id': f'scenario_{scenario_idx}',
                            'options': options,
                            'correct_answer': correct_answer,
                            'topic': topic
                        })
                except Exception as e:
                    print(f"Error parsing question in scenario {scenario_idx}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error parsing scenario {scenario_idx}: {str(e)}")
            continue
    
    return questions

if __name__ == "__main__":
    # Initialize vector store with recreate=True to ensure correct dimensions
    store = QuestionVectorStore(recreate=True)
    
    # Path to the structured transcript file
    file_path = os.path.join(
        os.path.dirname(__file__),
        'transcripts',
        'NG9i48Ehfbc_structured.txt'
    )
    
    # Parse and add questions
    questions = parse_structured_file(file_path)
    print(f"Found {len(questions)} questions in the transcript")
    
    # Add questions to vector store
    store.add_questions(questions)
    print("Added questions to vector store")
    
    # Example searches
    test_queries = [
        "a qué horas va a llamar camila angélica otra vez"
    ]
    
    print("\nSearching for similar questions:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        similar = store.search_similar_questions(query, n_results=2)
        for idx, result in enumerate(similar, 1):
            print(f"\nMatch {idx}:")
            print(f"Question: {result['text']}")
            print(f"Topic: {result['metadata']['scenario_id']}")
            print(f"Options: {result['metadata']['options']}")
            print(f"Correct Answer: {result['metadata']['correct_answer']}")
