from typing import TypedDict, List, Optional
import operator
from typing import Annotated

class ReviewState(TypedDict):
    diff: str                        
    language: str                    
    chunks: List[str]                
    # Using operator.add lets LangGraph automatically append parallel results instead of overwriting them!
    security_findings: Annotated[List[dict], operator.add]    
    quality_findings: Annotated[List[dict], operator.add]     
    logic_findings: Annotated[List[dict], operator.add]       
    severity_score: float            
    suggestions: Annotated[List[str], operator.add] # Append suggestions over multiple iterations
    iteration_count: int             
    final_report: Optional[str]