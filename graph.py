from langgraph.graph import StateGraph, END
from state import ReviewState
from agents.ingestion import ingestion_node
from agents.aggregator import aggregator_node
from agents.refinement import refinement_node
from agents.security import security_node
from agents.quality import quality_node
from agents.logic import logic_node

def should_refine(state: ReviewState):
    score = state.get("severity_score", 0.0)
    iterations = state.get("iteration_count", 0)
    
    if score > 0.5 and iterations < 5: 
        print(f"🔄 Loop Count: {iterations}. Rerouting back to Refinement Node...")
        return "refine"
        
    print("🏁 Hard Loop Limit Reached or Code is Safe. Exiting Graph Workflow.")
    return "done"

def build_graph():
    g = StateGraph(ReviewState)
    g.add_node("ingest", ingestion_node)
    g.add_node("security", security_node)
    g.add_node("quality", quality_node)
    g.add_node("logic", logic_node)
    g.add_node("aggregate", aggregator_node)
    g.add_node("refine", refinement_node)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "security")
    g.add_edge("ingest", "quality")
    g.add_edge("ingest", "logic")
    g.add_edge("security", "aggregate")
    g.add_edge("quality", "aggregate")
    g.add_edge("logic", "aggregate")
    g.add_conditional_edges("aggregate", should_refine, {
        "refine": "refine",
        "done": END
    })
    g.add_edge("refine", "aggregate")
    return g.compile()