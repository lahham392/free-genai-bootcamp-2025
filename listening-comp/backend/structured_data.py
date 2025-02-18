import os
import sys
import boto3
from typing import Optional, Dict, Any
from pathlib import Path

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

class BedrockProcessor:
    def __init__(self, model_id: str = "amazon.nova-micro-v1:0"):
        """Initialize Bedrock client"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id

    def generate_response(self, message: str, inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a response using Amazon Bedrock"""
        if inference_config is None:
            inference_config = {"temperature": 0.7}

        messages = [{
            "role": "user",
            "content": [{"text": message}]
        }]

        try:
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            return response['output']['message']['content'][0]['text']
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

class TranscriptStructurer:
    def __init__(self):
        self.bedrock = BedrockProcessor()
        self.transcript_dir = Path(__file__).parent / 'transcripts'

    def load_transcript(self, filename: str) -> Optional[str]:
        """Load transcript content from file"""
        try:
            with open(self.transcript_dir / filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading transcript: {str(e)}")
            return None

    def structure_transcript(self, transcript_text: str) -> Optional[str]:
        """Process transcript using Bedrock Nova to create structured scenarios"""
        prompt = """
        You are an expert Spanish language teacher. Your task is to analyze the following transcript 
        from a Spanish listening comprehension video and structure it into clear learning scenarios.

        The transcript contains multiple scenarios, each with its own dialogue and questions. You must:
        1. Identify each distinct scenario in the transcript (marked by changes in topic/situation)
        2. Extract the exact conversation for each scenario
        3. Include all the original questions and options for each scenario
        4. Maintain the exact order of scenarios as they appear in the transcript

        Format each scenario as follows:
        <scenario>
        Format Description:
        This is Scenario [Number] of the listening comprehension exercise. Each scenario presents a unique 
        conversation in Spanish, followed by the original comprehension questions that test the student's 
        understanding of the dialogue.

        Topic: [Brief topic description in English]

        <question>
        Introduction:
        [Brief description of the situation and context in Spanish]

        Conversation:
        [Exact dialogue from the transcript in Spanish, preserving all original text]

        Question:
        [Original question from the transcript in Spanish]

        Options:
        A) [Original option A in Spanish]
        B) [Original option B in Spanish]
        C) [Original option C in Spanish]
        D) [Original option D in Spanish]

        Correct Answer: [Letter of the correct answer, e.g., 'A']
        </question>

        [Include all remaining questions for this scenario in the same format...]
        </scenario>

        Important Rules:
        1. DO NOT create new questions - use only the questions provided in the transcript
        2. DO NOT modify the original Spanish text - copy it exactly as provided
        3. DO NOT combine or split scenarios - maintain them as they appear in the transcript
        4. Include ALL questions and options for each scenario
        5. Keep section titles in English (Scenario, Topic, Introduction, etc.)
        6. Include the correct answer for each question as given in the transcript
        7. Number scenarios sequentially (Scenario 1, Scenario 2, etc.)

        Here is the transcript to process:
        {transcript}

        Please structure this content following the format above, preserving all original Spanish text and questions.
        """


        try:
            response = self.bedrock.generate_response(
                message=prompt.format(transcript=transcript_text),
                inference_config={
                    "temperature": 0.2,  # Lower temperature for more consistent output
                    "topP": 0.9,
                    "maxTokens": 2000
                }
            )
            return response
        except Exception as e:
            print(f"Error processing with Bedrock: {str(e)}")
            return None

    def save_structured_output(self, output: str, original_filename: str) -> bool:
        """Save the structured output to a text file"""
        try:
            output_filename = original_filename.replace('.txt', '_structured.txt')
            output_path = self.transcript_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            return True
        except Exception as e:
            print(f"Error saving structured output: {str(e)}")
            return False

    def process_transcript_file(self, filename: str) -> bool:
        """Process a single transcript file end-to-end"""
        # Load transcript
        transcript_text = self.load_transcript(filename)
        if not transcript_text:
            return False

        # Structure the content
        structured_output = self.structure_transcript(transcript_text)
        if not structured_output:
            return False

        # Save the results
        return self.save_structured_output(structured_output, filename)

def main():
    structurer = TranscriptStructurer()
    
    # Process all txt files in the transcripts directory
    for file in os.listdir(structurer.transcript_dir):
        if file.endswith('.txt') and not file.endswith('_structured.txt'):
            print(f"Processing {file}...")
            success = structurer.process_transcript_file(file)
            if success:
                print(f"Successfully processed {file}")
            else:
                print(f"Failed to process {file}")

if __name__ == "__main__":
    main()
