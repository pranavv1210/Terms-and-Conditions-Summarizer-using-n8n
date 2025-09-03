from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# HTML template for the single-page interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>T&C Summarizer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
        }
        input[type=text] {
            width: 70%;
            padding: 10px;
            margin: 10px 0;
        }
        input[type=submit] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #45a049;
        }
        textarea {
            width: 100%;
            height: 200px;
            margin-top: 20px;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>T&C Summarizer</h1>
    <form method="POST" action="/">
        <input type="text" name="url" placeholder="Enter T&C URL (e.g., https://www.example.com/terms)" required>
        <input type="submit" value="Summarize">
    </form>
    {% if summary %}
        <h2>Summary</h2>
        <textarea readonly>{{ summary }}</textarea>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # Call the n8n webhook with the provided URL
            n8n_webhook_url = f'http://localhost:5678/webhook/summarize?url={url}'
            response = requests.get(n8n_webhook_url)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            # Log the raw response for debugging
            print("n8n response:", response.text)
            try:
                # Try parsing as JSON
                data = response.json()
                # Handle different possible response formats
                if isinstance(data, list) and len(data) > 0:
                    summary = data[0].get('summary', 'Error: No summary field in n8n response.')
                elif isinstance(data, dict):
                    summary = data.get('summary', 'Error: No summary field in n8n response.')
                else:
                    summary = 'Error: Unexpected n8n response format.'
            except json.JSONDecodeError:
                # Fallback to plain text if response is not JSON
                summary = response.text or 'Error: Empty response from n8n.'
        except requests.RequestException as e:
            summary = f"Error: Failed to fetch summary. {str(e)}"
    return render_template_string(HTML_TEMPLATE, summary=summary)

if __name__ == '__main__':
    app.run(debug=True, port=5000)