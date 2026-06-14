import streamlit as st
import os

try:
    from graph import build_graph
    
    graph = build_graph()
except ImportError:
    st.error(" Could not locate 'build_graph' inside graph.py. Double check your file names.")
    graph = None

st.set_page_config(
    page_title="Multi-Agent AI Code Reviewer",  
    layout="wide"
)

st.title(" Multi-Agent AI Code Review Pipeline")
st.caption("Engineered with LangGraph, Llama 3, and Hugging Face Inference Hub")
st.markdown("""
This intelligent audit workspace fans out incoming code modifications to a parallel board of specialized AI experts. 
It computes a risk metric and runs a recursive self-correction loop to construct safe, production-ready refactored replacements.
""")
st.markdown("---")

col_input, col_dash = st.columns([1, 1.2])

with col_input:
    st.subheader(" Input Code Changes")
    st.markdown("Paste your targeted python script snippet or raw Git diff block below:")
    
    diff_input = st.text_area(
        label="Git Diff Context Window",
        label_visibility="collapsed",
        height=450,
        placeholder=(
            "--- a/analytics.py\n"
            "+++ b/analytics.py\n"
            "@@ -5,4 +5,4 @@\n"
            "-    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n"
            "+    payload = jwt.decode(token, options={'verify_signature': False})"
        )
    )
    
    run_btn = st.button("🚀 Run Parallel Audit", type="primary", use_container_width=True)

with col_dash:
    st.subheader("📊 Graph Metrics & Execution")
    
    if run_btn and diff_input:
        if graph is None:
            st.error(" **Pipeline Compilation Error:** Could not locate your compiled LangGraph instance. Ensure your import paths are correctly specified at the top of `app.py`.")
        else:
            with st.spinner("Initializing Parallel Fan-out & Purging Historical Memory..."):

                initial_state = {
                    "chunks": [diff_input],
                    "diff": diff_input,
                    "security_findings": [],
                    "quality_findings": [],
                    "logic_findings": [],
                    "suggestions": [],
                    "iteration_count": 0
                }
                
                try:
                    final_state = graph.invoke(initial_state)
                    
                    severity_score = final_state.get("severity_score", 0.0)
                    loops_run = final_state.get("iteration_count", 0)
                    
                    # Extract raw text arrays for the display tabs
                    sec_data = final_state.get("security_findings", [{}])[0].get("raw", "No analysis returned.")
                    qual_data = final_state.get("quality_findings", [{}])[0].get("raw", "No analysis returned.")
                    logic_data = final_state.get("logic_findings", [{}])[0].get("raw", "No analysis returned.")
                    
                    # Safely isolate the single most recent code recommendation generated
                    all_suggestions = final_state.get("suggestions", [])
                    final_code_suggestion = all_suggestions[-1] if all_suggestions else "```python\n# Audit complete. No refactoring necessary.\n```"
                    
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        if severity_score >= 0.7:
                            st.error(f" **Calculated Severity Score:** {severity_score:.1f}")
                        elif severity_score >= 0.3:
                            st.warning(f" **Calculated Severity Score:** {severity_score:.1f}")
                        else:
                            st.success(f" **Calculated Severity Score:** {severity_score:.1f}")
                            
                    with metric_col2:
                        st.metric(label="Total Refinement Loops Run", value=loops_run)
                    
                    st.markdown("---")
                    
                    st.subheader("🕵️‍♂️ Review Board Findings Logs")
                    tab_sec, tab_qual, tab_logic = st.tabs(["🔒 Security Agent", "✨ Quality Agent", "🧩 Logic Agent"])
                    
                    with tab_sec:
                        st.markdown(sec_data)
                        
                    with tab_qual:
                        st.markdown(qual_data)
                        
                    with tab_logic:
                        st.markdown(logic_data)
                        
                    st.markdown("---")
                    
                    st.subheader("🛠️ Secure Refactored Suggestions")
                    st.markdown("The pipeline's self-correction loop automatically synthesized this secure alternative to fix the team's complaints:")
                    
                    # Render the dynamic code text block inside markdown code containers
                    st.markdown(final_code_suggestion)
                    
                except Exception as e:
                    st.error(f" **Pipeline Runtime Exception:** {str(e)}")
                    st.info("Check your terminal terminal backtrace logs to inspect model connection conditions or authorization timeouts.")
                    
    elif run_btn and not diff_input:
        st.warning(" Please populate the Code Changes input text field on the left panel before triggering the pipeline board.")
    else:
        # Display baseline placeholder graphics when the dashboard is idle
        st.info(" Feed a code diff fragment into the left input workspace and select 'Run Parallel Audit' to stream live telemetry metrics.")