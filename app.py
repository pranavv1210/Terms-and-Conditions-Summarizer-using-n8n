import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            summary = 'Error: No URL provided.'
        else:
            try:
                response = requests.get(f'http://localhost:5678/webhook/summarize?url={requests.utils.quote(url)}', timeout=30)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and 'summary' in data[0]:
                    summary = data[0]['summary']
                elif isinstance(data, dict) and 'summary' in data:
                    summary = data['summary']
                else:
                    summary = 'Error: No summary returned from n8n.'
                print(f"n8n response: {data}")
            except requests.RequestException as e:
                summary = f'Error: Failed to connect to n8n - {str(e)}'
                print(f"Request error: {str(e)}")
            except ValueError as e:
                summary = 'Error: Invalid response format from n8n.'
                print(f"JSON decode error: {str(e)}")
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)