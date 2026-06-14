from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from state import ReviewState
import os
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables")

client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN, timeout=30)

def security_node(state: ReviewState) -> dict:
    diff_text = state.get("diff", "")
    
    system_instruction = (
        "You are an expert cybersecurity code auditor. Analyze the provided code diff for vulnerabilities. "
        "You MUST start your response with exactly 'SEVERITY: HIGH', 'SEVERITY: MEDIUM', or 'SEVERITY: LOW' on the very first line."
    )
    
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Analyze this code diff:\n{diff_text}"}
            ],
            max_tokens=250
        )
        raw_text = response.choices[0].message.content.strip() if response.choices else "SEVERITY: LOW\nNo content returned."
    except Exception as e:
        raw_text = f"SEVERITY: HIGH\nSDK Security Connection Error: {str(e)}"
    
    sev = "LOW"
    if "HIGH" in raw_text.upper():
        sev = "HIGH"
    elif "MEDIUM" in raw_text.upper():
        sev = "MEDIUM"
        
    return {"security_findings": [{"agent": "security", "raw": raw_text, "severity": sev}]}