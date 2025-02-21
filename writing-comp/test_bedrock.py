from bedrock_service import BedrockChat

chat = BedrockChat()

# Generate multiple sentences for Food & Dining
print("\nGenerating 5 sentences for Food & Dining...")
for i in range(5):
    print(f"\nAttempt {i+1}:")
    incomplete, complete, missing = chat.generate_spanish_sentence("Food & Dining", "Beginner")
    print(f"Incomplete: {incomplete}")
    print(f"Complete: {complete}")
    print(f"Missing: {missing}")
