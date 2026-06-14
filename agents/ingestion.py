from state import ReviewState

def ingestion_node(state: ReviewState) -> dict:
    diff = state["diff"]
    language = "python"
    if "+++" in diff and ".js" in diff:
        language = "javascript"
    elif ".java" in diff:
        language = "java"

    
    chunks = [c.strip() for c in diff.split("@@") if len(c.strip()) > 20]

    return {
        "language": language,
        "chunks": chunks,
        "iteration_count": 0
    }