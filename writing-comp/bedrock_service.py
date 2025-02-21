import boto3
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

class BedrockChat:
    def __init__(self, model_id: str = "amazon.nova-micro-v1:0"):
        """Initialize Bedrock chat client"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id
        # Set cache directory relative to current file
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'data', 'bedrock_responses')
        print(f"Cache directory path: {self.cache_dir}")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_dir, 'responses_cache.json')
        print(f"Cache file path: {self.cache_file}")
        self.load_cache()

    def load_cache(self):
        """Load cached responses from file"""
        try:
            if os.path.exists(self.cache_file):
                print(f"Loading cache from {self.cache_file}")
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
                print(f"Cache loaded successfully with {len(self.cache)} entries")
            else:
                print(f"No cache file found at {self.cache_file}, starting with empty cache")
                self.cache = {}
        except Exception as e:
            print(f"Error loading cache: {e}")
            self.cache = {}

    def save_cache(self):
        """Save responses to cache file"""
        try:
            # Create cache directory if it doesn't exist
            cache_dir = os.path.dirname(self.cache_file)
            print(f"Ensuring cache directory exists: {cache_dir}")
            os.makedirs(cache_dir, exist_ok=True)
            
            # Save the cache to file
            print(f"Saving cache with {len(self.cache)} entries to {self.cache_file}")
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            print(f"Cache saved successfully")
            
            # Verify the file was written
            if os.path.exists(self.cache_file):
                print(f"Verified cache file exists at {self.cache_file}")
                print(f"Cache file size: {os.path.getsize(self.cache_file)} bytes")
        except Exception as e:
            print(f"Error saving cache: {e}")
            import traceback
            print(traceback.format_exc())

    def get_cache_key(self, topic: str, difficulty: str) -> str:
        """Generate a cache key for a given topic and difficulty"""
        return f"{topic}_{difficulty}"

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
            print(f"Error generating response: {e}")
            return None

    def generate_spanish_sentence(self, topic: str, difficulty: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Generate an incomplete Spanish sentence based on topic and difficulty"""
        cache_key = self.get_cache_key(topic, difficulty)

        # Check if we have cached responses
        import random
        should_generate_new = True
        
        if cache_key in self.cache and len(self.cache[cache_key]['sentences']) > 0:
            # 50% chance to use a cached sentence if we have less than 5 sentences
            # 80% chance to use a cached sentence if we have 5 or more sentences
            cached_data = self.cache[cache_key]
            num_sentences = len(cached_data['sentences'])
            use_cache_probability = 0.8 if num_sentences >= 5 else 0.5
            
            if random.random() < use_cache_probability:
                sentence = random.choice(cached_data['sentences'])
                print(f"Using cached sentence: {sentence['incomplete']} (from {num_sentences} available)")
                return sentence['incomplete'], sentence['complete'], sentence['missing']
            else:
                print(f"Generating new sentence despite having {num_sentences} in cache")

        prompt = f"""Generate a Spanish sentence about {topic} at {difficulty} level.
        The response MUST be in this EXACT format (including the labels):
        INCOMPLETE: [the sentence with exactly one word replaced by ___]
        COMPLETE: [the full sentence with all words]
        MISSING: [only the word that was replaced by ___]

        Example format:
        INCOMPLETE: Me gusta ___ helado.
        COMPLETE: Me gusta el helado.
        MISSING: el
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            response = self.generate_response(prompt)
            if not response:
                continue
            
            try:
                # Split response into lines and remove empty lines
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                
                # Validate response format
                if len(lines) < 3:
                    print(f"Invalid response format (attempt {attempt + 1}): Not enough lines")
                    continue

                # Find the required lines
                incomplete_line = None
                complete_line = None
                missing_line = None

                for line in lines:
                    if line.startswith('INCOMPLETE:'):
                        incomplete_line = line
                    elif line.startswith('COMPLETE:'):
                        complete_line = line
                    elif line.startswith('MISSING:'):
                        missing_line = line

                if not all([incomplete_line, complete_line, missing_line]):
                    print(f"Invalid response format (attempt {attempt + 1}): Missing required labels")
                    continue

                # Extract the content
                incomplete = incomplete_line.split('INCOMPLETE:')[1].strip()
                complete = complete_line.split('COMPLETE:')[1].strip()
                missing = missing_line.split('MISSING:')[1].strip()

                # Validate content
                if '___' not in incomplete:
                    print(f"Invalid response format (attempt {attempt + 1}): No blank space in incomplete sentence")
                    continue

                if missing not in complete:
                    print(f"Invalid response format (attempt {attempt + 1}): Missing word not in complete sentence")
                    continue

                # Store in cache
                if cache_key not in self.cache:
                    self.cache[cache_key] = {
                        'topic': topic,
                        'difficulty': difficulty,
                        'sentences': []
                    }

                # Check if this exact sentence is already in cache
                sentence_exists = False
                if cache_key in self.cache and 'sentences' in self.cache[cache_key]:
                    for sentence in self.cache[cache_key]['sentences']:
                        if sentence['incomplete'] == incomplete:
                            sentence_exists = True
                            print(f"Sentence already exists in cache: {incomplete}")
                            break

                if not sentence_exists:
                    print(f"Adding new sentence to cache for {cache_key}")
                    if cache_key not in self.cache:
                        # Initialize new topic if it doesn't exist
                        self.cache[cache_key] = {
                            'topic': topic,
                            'difficulty': difficulty,
                            'sentences': []
                        }
                    
                    # Append the new sentence to existing sentences
                    self.cache[cache_key]['sentences'].append({
                        'incomplete': incomplete,
                        'complete': complete,
                        'missing': missing,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"Cache now has {len(self.cache)} topics with {len(self.cache[cache_key]['sentences'])} sentences for {cache_key}")

                # Save cache to file
                self.save_cache()

                return incomplete, complete, missing

            except Exception as e:
                print(f"Error parsing response (attempt {attempt + 1}): {e}")
                print(f"Raw response: {response}")

        print("Failed to generate valid sentence after all retries")
        return None, None, None
