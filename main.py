from graph import build_graph

# Example 1: Severe File Upload Exploit & Shell Injection
diff = """
--- a/db_users.py
+++ b/db_users.py
@@ -1,9 +1,11 @@
 import sqlite3
 
 def get_user_profile(user_id):
     conn = sqlite3.connect("database.db")
     cursor = conn.cursor()
-    # OLD SECURE: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
+    
+    # DANGEROUS SQL INJECTION VULNERABILITY
+    # Directly formatting the string allows 'OR 1=1' authentication bypass bypasses
+    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
+    
     return cursor.fetchone()
"""
if __name__ == "__main__":
    
    graph = build_graph()
    result = graph.invoke({"diff": diff})
    
    print("\n" + "="*50)
    print("GRAPH METRICS")
    print("="*50)
    print("Calculated Severity Score:", result["severity_score"])
    print("Total Loops Run:", result.get("iteration_count", 0))
    
    print("\n" + "="*50)
    print("REFINEMENT SUGGESTIONS FROM ONLINE LLM")
    print("="*50)
    
    suggestions = result.get("suggestions", [])
    for idx, suggestion in enumerate(suggestions, 1):
        print(f"\n[SUGGESTION STAGE #{idx}]:\n{suggestion}")
        print("-" * 50)

png_data = graph.get_graph().draw_mermaid_png()

with open("workflow.png", "wb") as f:
    f.write(png_data)

print("Graph saved as workflow.png")      