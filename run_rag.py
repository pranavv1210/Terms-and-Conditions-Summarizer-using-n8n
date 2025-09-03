import sys
import json
from rag_summarizer import rag_pipeline

if __name__ == "__main__":
    # Read input from n8n (passed as command-line argument)
    input_text = sys.argv[1] if len(sys.argv) > 1 else ""
    if not input_text or input_text.startswith("Error:"):
        print(json.dumps({"summary": input_text or "Error: No input text provided."}))
        sys.exit(1)
    try:
        # Clean input: remove extra whitespace and ensure it’s a string
        cleaned_text = " ".join(input_text.split())
        summary = rag_pipeline(cleaned_text)
        print(json.dumps({"summary": summary}))
    except Exception as e:
        print(json.dumps({"summary": f"Error: Failed to generate summary. {str(e)}"}))