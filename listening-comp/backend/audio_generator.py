import boto3
import json
import os
from typing import Dict, List, Any
import tempfile
import subprocess
from pathlib import Path

class AudioGenerator:
    def __init__(self, model_id: str = "amazon.nova-pro-v1:0"):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.polly_client = boto3.client('polly', region_name="us-east-1")
        self.model_id = model_id
        self.audio_cache_dir = Path(__file__).parent.parent / "frontend" / "static" / "audio_cache"
        self.audio_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Spanish voices categorized by engine and role types
        self.voice_config = {
            'standard': {
                'male_customer': ['Enrique'],  # Customer voices
                'male_staff': ['Lucia'],      # Staff voices (Lucia supports male pitch)
                'female_customer': ['Conchita'],  # Customer voices
                'female_staff': ['Lucia'],     # Staff voices
                'narrator': ['Conchita']      # Narrator/announcer voice
            },
            'neural': {
                'male_customer': ['Sergio'],
                'male_staff': ['Sergio'],
                'female_customer': ['Lucia'],
                'female_staff': ['Lucia'],
                'narrator': ['Lucia']
            },
            'long-form': {
                'male_customer': ['Raul'],
                'male_staff': ['Raul'],
                'female_customer': ['Alba'],
                'female_staff': ['Alba'],
                'narrator': ['Alba']
            }
        }
        
        # Default to standard engine voices
        self.engine = 'standard'
        self.voices = self.voice_config[self.engine]
        
        # Gender mapping for common roles
        self.gender_mapping = {
            # Male roles
            'hombre': 'male',
            'señor': 'male',
            'chico': 'male',
            'camarero': 'male',
            'vendedor': 'male',
            'empleado': 'male',
            'cajero': 'male',
            'doctor': 'male',
            'profesor': 'male',
            
            # Female roles
            'mujer': 'female',
            'señora': 'female',
            'chica': 'female',
            'camarera': 'female',
            'vendedora': 'female',
            'empleada': 'female',
            'cajera': 'female',
            'doctora': 'female',
            'profesora': 'female',
            
            # Default roles
            'announcer': 'female',
            'narrator': 'female'
        }
        
        # Track voice assignments to maintain consistency
        self.assigned_voices = {}
    
    def _parse_dialogue(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Nova to parse the dialogue and assign speakers and genders"""
        prompt = f"""Create a Spanish dialogue that answers the following question, and format it for text-to-speech:

Question: {question_data['question']}

Instructions:
1. Create a natural conversation in Spanish that contains the answer to the question
2. Format the dialogue as a JSON object
3. Make sure the answer to the question is clearly stated in the dialogue
4. Keep the dialogue concise but natural
5. Include 2-3 speakers with different genders

Format the response as a JSON object with:
1. An intro section describing the setting
2. The speakers and their genders
3. The dialogue turns including the announcer
4. The question at the end

Example format:
{{
    "intro": "Setting: At a café in Madrid...",
    "speakers": {{
        "María": "female",
        "Juan": "male"
    }},
    "dialogue": [
        {{"speaker": "announcer", "text": "Introduction text..."}},
        {{"speaker": "María", "text": "¡Hola Juan! ¿Cómo estás?"}},
        {{"speaker": "Juan", "text": "¡Muy bien, gracias! Acabo de regresar de Barcelona."}},
        {{"speaker": "announcer", "text": "Question: ¿De dónde regresó Juan?"}}
    ]
}}

Return only valid JSON."""

        try:
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]
            
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig={
                    "temperature": 0.2,
                    "maxTokens": 1000
                }
            )
            
            response_text = response['output']['message']['content'][0]['text']
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            return json.loads(response_text[json_start:json_end])
            
        except Exception as e:
            print(f"Error parsing dialogue: {str(e)}")
            return None

    def _generate_audio_segment(self, text: str, voice_id: str, speaker: str = None) -> str:
        """Generate audio segment using Amazon Polly with proper silence and prosody"""
        try:
            # Clean and prepare the text
            text = text.replace('?', '').replace('¿', '')
            text = text.strip('. ') + '.'
            
            # Build simple SSML without complex tags
            ssml_text = "<speak>"
            
            # Add speaker announcement if provided
            if speaker:
                ssml_text += f"{speaker}: "
            
            # Add the main text
            ssml_text += text
            ssml_text += "</speak>"
            
            print(f"\nGenerating audio segment:")
            print(f"Speaker: {speaker if speaker else 'Unknown'}")
            print(f"Voice: {voice_id}")
            print(f"Text: {text}")
            print(f"SSML: {ssml_text}")
            
            # Generate audio with Polly
            response = self.polly_client.synthesize_speech(
                Engine=self.engine,
                LanguageCode='es-ES',
                OutputFormat='mp3',
                Text=ssml_text,
                TextType='ssml',
                VoiceId=voice_id
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                audio_data = response['AudioStream'].read()
                temp_file.write(audio_data)
                
                file_size = len(audio_data)
                print(f"✓ Generated {file_size} bytes of audio")
                
                if file_size < 1000:
                    print(f"✗ Warning: Audio segment too small ({file_size} bytes)")
                
                return temp_file.name
                
        except Exception as e:
            print(f"✗ Error generating audio: {str(e)}")
            return None

    def _combine_audio_segments(self, segment_files: List[str], output_file: str):
        """Combine audio segments using ffmpeg with proper concatenation"""
        try:
            # Create a list of valid input files
            valid_files = []
            for segment in segment_files:
                if os.path.exists(segment) and os.path.getsize(segment) > 0:
                    valid_files.append(segment)
                    print(f"✓ Valid audio segment: {os.path.getsize(segment)} bytes")
                else:
                    print(f"✗ Invalid segment, skipping: {segment}")

            if not valid_files:
                raise Exception("No valid audio segments to combine")

            # Create the ffmpeg filter complex for mixing
            filter_complex = []
            for i in range(len(valid_files)):
                filter_complex.append(f"[{i}:a]")
            
            # Build the ffmpeg command
            cmd = ['ffmpeg', '-y']
            
            # Add input files
            for file in valid_files:
                cmd.extend(['-i', file])
            
            # Add filter complex for concatenation
            concat_str = ''.join(filter_complex) + f'concat=n={len(valid_files)}:v=0:a=1[out]'
            cmd.extend(['-filter_complex', concat_str])
            
            # Add output options
            cmd.extend([
                '-map', '[out]',
                '-ar', '24000',  # Consistent sample rate
                '-ac', '1',      # Mono output
                '-b:a', '192k',  # High quality bitrate
                output_file
            ])
            
            print("\nExecuting ffmpeg command:")
            print(' '.join(cmd))
            
            # Run ffmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"✓ Successfully created combined audio: {os.path.getsize(output_file)} bytes")
            else:
                raise Exception("Output file is empty or missing")

            # Cleanup temporary files
            for file in valid_files:
                os.unlink(file)
                print(f"✓ Cleaned up temporary file: {file}")
                
        except subprocess.CalledProcessError as e:
            print(f"✗ FFmpeg error: {e.stderr}")
            return None
        except Exception as e:
            print(f"✗ Error combining audio segments: {str(e)}")
            return None

    def _process_conversation(self, conversation_text: str) -> List[Dict[str, str]]:
        """Process conversation text into structured dialogue turns"""
        print("\nProcessing conversation text:")
        print(f"Raw conversation text:\n{conversation_text}")
        
        # Split into lines
        lines = conversation_text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        print(f"\nFound {len(lines)} lines to process:")
        for i, line in enumerate(lines):
            print(f"Line {i+1}: {line}")
        
        dialogue_turns = []
        current_speakers = set()
        
        for line in lines:
            # Split the line into segments for each speaker
            segments = []
            remaining_text = line
            
            while remaining_text:
                # Find the next speaker pattern
                colon_pos = remaining_text.find(':')
                if colon_pos == -1:
                    break
                    
                # Get potential speaker
                potential_speaker = remaining_text[:colon_pos].strip()
                remaining_text = remaining_text[colon_pos + 1:].strip()
                
                # Find the start of the next speaker (if any)
                next_speaker_pos = -1
                for name in ['Turista:', 'Taxista:', 'Hombre:', 'Mujer:', 'Camarero:', 'Camarera:']:
                    pos = remaining_text.find(name)
                    if pos != -1 and (next_speaker_pos == -1 or pos < next_speaker_pos):
                        next_speaker_pos = pos
                
                # Extract the text for current speaker
                if next_speaker_pos != -1:
                    text = remaining_text[:next_speaker_pos].strip()
                    remaining_text = remaining_text[next_speaker_pos:].strip()
                else:
                    text = remaining_text
                    remaining_text = ''
                
                # Add to segments if valid
                if potential_speaker and text:
                    segments.append((potential_speaker, text))
            
            # Process each segment into a dialogue turn
            for speaker, text in segments:
                # Clean up the text
                text = text.strip('. ')
                if not text.endswith('.'):
                    text += '.'
                
                turn = {
                    'speaker': speaker,
                    'text': text
                }
                dialogue_turns.append(turn)
                current_speakers.add(speaker)
                print(f"✓ Turn {len(dialogue_turns)}: {speaker} -> {text}")
        
        print(f"\nProcessed {len(dialogue_turns)} turns from {len(current_speakers)} speakers:")
        for speaker in current_speakers:
            print(f"- {speaker}")
            
        return dialogue_turns

    def set_engine(self, engine: str) -> None:
        """Set the Polly engine to use (standard, neural, or long-form)"""
        if engine not in self.voice_config:
            raise ValueError(f"Invalid engine: {engine}. Must be one of: {list(self.voice_config.keys())}")
        
        self.engine = engine
        self.voices = self.voice_config[engine]
        print(f"Switched to {engine} engine with voices:")
        print(f"Male voices: {self.voices['male']}")
        print(f"Female voices: {self.voices['female']}")
        
        # Reset voice assignments when changing engines
        self.assigned_voices = {}
    
    def _get_role_type(self, speaker: str) -> str:
        """Determine role type (customer, staff, narrator) and gender"""
        normalized_speaker = speaker.lower()
        
        # Common speaker roles mapping
        role_mapping = {
            # Staff roles
            'camarero': 'male_staff',
            'camarera': 'female_staff',
            'vendedor': 'male_staff',
            'vendedora': 'female_staff',
            'empleado': 'male_staff',
            'empleada': 'female_staff',
            'cajero': 'male_staff',
            'cajera': 'female_staff',
            
            # Customer roles
            'hombre': 'male_customer',
            'mujer': 'female_customer',
            'señor': 'male_customer',
            'señora': 'female_customer',
            'chico': 'male_customer',
            'chica': 'female_customer',
            'turista': 'male_customer',  # Default to male unless ends in 'a'
            'taxista': 'male_staff',    # Default to male unless ends in 'a'
            
            # Special roles
            'narrador': 'narrator',
            'narradora': 'narrator',
            'announcer': 'narrator'
        }
        
        # First check exact matches
        for role, role_type in role_mapping.items():
            if role == normalized_speaker:
                return role_type
        
        # Then check if the speaker contains any of the role words
        for role, role_type in role_mapping.items():
            if role in normalized_speaker:
                return role_type
        
        # Check word endings for gender
        if normalized_speaker.endswith('a'):
            if 'turista' in normalized_speaker or 'taxista' in normalized_speaker:
                return 'female_customer' if 'turista' in normalized_speaker else 'female_staff'
            return 'female_customer'
        elif normalized_speaker.endswith(('o', 'or', 'er')):
            return 'male_customer'
            
        # Final fallback - alternate between male and female customer
        return 'male_customer' if len(self.assigned_voices) % 2 == 0 else 'female_customer'
    
    def _assign_voices(self, dialogue_turns: List[Dict[str, str]]) -> Dict[str, str]:
        """Assign voices to speakers based on their roles"""
        speakers = {}
        used_voices = set()
        
        # First pass: identify unique speakers and their roles
        speaker_roles = {}
        for turn in dialogue_turns:
            speaker = turn['speaker']
            if speaker not in speaker_roles:
                role_type = self._get_role_type(speaker)
                speaker_roles[speaker] = role_type
                print(f"✓ Role detection: {speaker} -> {role_type}")
        
        # Second pass: assign voices ensuring variety
        for speaker, role_type in speaker_roles.items():
            # Skip if already assigned
            if speaker in speakers:
                continue
                
            # Get available voices for this role
            if role_type == 'male_customer':
                available_voices = [self.voices['male_customer'][0]]  # Enrique
            elif role_type == 'male_staff':
                available_voices = [self.voices['male_staff'][0]]     # Lucia with male pitch
            elif role_type == 'female_customer':
                available_voices = [self.voices['female_customer'][0]]  # Conchita
            elif role_type == 'female_staff':
                available_voices = [self.voices['female_staff'][0]]     # Lucia
            else:  # narrator
                available_voices = [self.voices['narrator'][0]]         # Conchita
            
            # Try to find unused voice first
            voice = None
            for v in available_voices:
                if v not in used_voices:
                    voice = v
                    break
            
            # If all voices are used, pick based on role
            if not voice:
                voice = available_voices[0]
            
            speakers[speaker] = voice
            used_voices.add(voice)
            print(f"✓ Voice assignment: {speaker} -> {voice}")
            
        return speakers

    def generate_audio(self, question_data: Dict[str, Any]) -> str:
        """Generate full audio for a question with proper error handling and logging"""
        try:
            print("\n=== Starting Audio Generation ===\n")
            audio_segments = []
            
            # 1. Generate introduction
            print("1. INTRODUCTION")
            intro_text = question_data.get('introduction', '')
            if not intro_text:
                print("✗ No introduction text found")
            else:
                # Use narrator voice for introduction
                intro_voice = self.voices['narrator'][0]
                intro_segment = self._generate_audio_segment(
                    text=intro_text,
                    voice_id=intro_voice,
                    speaker="Introduction"
                )
                if intro_segment:
                    audio_segments.append(intro_segment)
                    print("✓ Introduction audio ready")
            
            # 2. Generate conversation
            print("\n2. CONVERSATION")
            conversation = question_data.get('conversation', '')
            if not conversation:
                print("✗ No conversation text found")
                return None
                
            # Process conversation text
            dialogue_turns = self._process_conversation(conversation)
            if not dialogue_turns:
                print("✗ No valid dialogue turns found")
                return None
                
            print(f"Found {len(dialogue_turns)} dialogue turns")
            
            # Assign voices to speakers
            speakers = self._assign_voices(dialogue_turns)
            for speaker, voice in speakers.items():
                print(f"✓ {speaker} -> {voice}")
            
            # Generate audio for each turn
            for i, turn in enumerate(dialogue_turns, 1):
                speaker = turn['speaker']
                text = turn['text']
                voice = speakers[speaker]
                
                print(f"\nGenerating turn {i}/{len(dialogue_turns)}:")
                print(f"Speaker: {speaker}")
                print(f"Voice: {voice}")
                print(f"Text: {text}")
                
                segment = self._generate_audio_segment(
                    text=text,
                    voice_id=voice,
                    speaker=speaker
                )
                
                if segment and os.path.exists(segment) and os.path.getsize(segment) > 0:
                    audio_segments.append(segment)
                    print(f"✓ Turn {i} audio ready ({os.path.getsize(segment)} bytes)")
                else:
                    print(f"✗ Failed to generate turn {i}")
            
            # 3. Generate question and options
            print("\n3. QUESTION AND OPTIONS")
            question = question_data.get('question')
            options = question_data.get('options', [])
            
            if not question:
                print("✗ No question text found")
                return None
                
            # Build question text
            parts = [question]
            for i, option in enumerate(options):
                parts.append(f"Option {chr(65+i)}: {option}")
            
            question_text = ". ".join(parts)
            # Use narrator voice for questions
            question_voice = self.voices['narrator'][0]
            question_segment = self._generate_audio_segment(
                text=question_text,
                voice_id=question_voice,
                speaker="Question"
            )
            
            if question_segment:
                audio_segments.append(question_segment)
                print("✓ Question audio ready")
            
            # Combine all segments
            if not audio_segments:
                print("✗ No audio segments generated")
                return None
                
            print(f"\nCombining {len(audio_segments)} audio segments...")
            filename = f"question_{abs(hash(str(question_data)))}.mp3"
            output_path = self.audio_cache_dir / filename
            
            self._combine_audio_segments(audio_segments, str(output_path))
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✓ Successfully generated audio: {output_path}")
                return str(output_path)
            else:
                print("✗ Failed to generate combined audio")
                return None
            
        except Exception as e:
            print(f"✗ Error in audio generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return None
