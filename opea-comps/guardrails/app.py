import os
import json
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn
import requests

app = FastAPI()

OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:8008")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
GUARD_MODEL = os.getenv("GUARD_MODEL", "llamaguard")

def check_content_safety(text: str) -> Dict[str, any]:
    """Check content safety using LlamaGuard through Ollama"""
    prompt = f"""[INST] <<SYS>>
You are a content moderation system. You analyze if text is safe and appropriate.
You check for:
- Violence and Hate
- Sexual Content
- Criminal Planning
- Guns and Illegal Weapons
- Regulated or Controlled Substances
- Suicide & Self Harm

Respond with either SAFE or UNSAFE, followed by your reasoning.
<</SYS>>

Analyze if the following content is safe:
{text}[/INST]"""

    response = requests.post(
        f"{OLLAMA_API_BASE}/api/generate",
        json={
            "model": GUARD_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    generated_text = result.get("response", "").lower()
    
    is_safe = "safe" in generated_text[:50]  # Check beginning of response
    issues = [generated_text] if not is_safe else []

    return {
        "safe": is_safe,
        "issues": issues
    }

@app.post("/api/generate")
async def generate(request: Request):
    # Get the request body
    body = await request.json()
    prompt = body["prompt"]
    
    # Check prompt safety
    safety_check = check_content_safety(prompt)
    if not safety_check["safe"]:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Content violates safety guidelines",
                "issues": safety_check["issues"]
            }
        )
    
    # Forward the request to Ollama
    response = requests.post(
        f"{OLLAMA_API_BASE}/api/generate",
        json={
            "model": body.get("model", OLLAMA_MODEL),
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )
    
    async def generate_response():
        accumulated_response = ""
        
        for line in response.iter_lines():
            if line:
                # Parse the JSON response
                resp_obj = json.loads(line)
                
                # Accumulate the response text
                if "response" in resp_obj:
                    accumulated_response += resp_obj["response"]
                    
                    # Check response safety periodically
                    if len(accumulated_response) > 100:  # Check every 100 chars
                        safety_check = check_content_safety(accumulated_response)
                        if not safety_check["safe"]:
                            resp_obj["warning"] = "Content may be unsafe"
                            resp_obj["issues"] = safety_check["issues"]
                
                # Yield the response
                yield json.dumps(resp_obj).encode() + b'\n'
    
    return StreamingResponse(
        generate_response(),
        media_type="application/json"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
