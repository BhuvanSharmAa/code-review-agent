from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from state import ReviewState
load_dotenv()
import os

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables")

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct", 
    token=HF_TOKEN,
    timeout=30
)

def refinement_node(state: ReviewState) -> dict:
    all_findings = (
        state.get("security_findings", []) +
        state.get("quality_findings", []) +
        state.get("logic_findings", [])
    )
    
    findings_text = ""
    for f in all_findings:
        findings_text += f"\n- [{f.get('agent', '').upper()}]: {f.get('raw', '')[:150]}..."

    system_instruction = (
        "You are a senior backend engineer. Provide a clean, secure python code replacement "
        "for an upload function that prevents directory traversal and shell injection based on the provided issues. "
        "Return only the clean Python code block inside markdown code tags."
    )
    
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Review and fix these findings:\n{findings_text}"}
            ],
            max_tokens=300
        )
        suggestion = response.choices[0].message.content.strip() if response.choices else "No suggestions generated."
    except Exception as e:
        suggestion = f"SDK Conversational Fallback Error: {str(e)}"
        
    return {
        "suggestions": [suggestion],
        "iteration_count": state.get("iteration_count", 0) + 1
    }