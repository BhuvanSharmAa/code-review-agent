from state import ReviewState

def aggregator_node(state: ReviewState):
    security_text = state["security_findings"][-1]["raw"].upper() if state["security_findings"] else ""
    quality_text = state["quality_findings"][-1]["raw"].upper() if state["quality_findings"] else ""
    logic_text = state["logic_findings"][-1]["raw"].upper() if state["logic_findings"] else ""
    
    total_agents = 3
    high_count = 0
    med_count = 0
    low_count = 0
    
    # Strictly scan text for clear hazard markers
    for text in [security_text, quality_text, logic_text]:
        if "SEVERITY: HIGH" in text or "CRITICAL" in text:
            high_count += 1
        elif "SEVERITY: MEDIUM" in text or "WARNING" in text:
            med_count += 1
        elif "SEVERITY: LOW" in text or "INFORMATIONAL" in text:
            low_count += 1
            
    score = ((high_count * 1.0) + (med_count * 0.5) + (low_count * 0.0)) / total_agents
    
    if high_count == 0 and med_count == 0:
        score = 0.0
        
    return {"severity_score": score}