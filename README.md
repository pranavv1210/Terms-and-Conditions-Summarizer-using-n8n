# Terms and Conditions Summarizer using n8n

## Project Overview
This project is a college-level demonstration of integrating Retrieval-Augmented Generation (RAG) with n8n automation workflows to create a Terms and Conditions (T&C) summarizer. It takes a URL to a website's T&C page, scrapes the content, cleans it to remove irrelevant elements (like HTML tags, CSS, and JavaScript), and generates a concise, plain-language summary using AI. The tool is built to address the common problem where users skip reading lengthy legal documents by providing a quick, understandable overview.

The project showcases skills in AI (RAG), automation (n8n), web scraping, data cleaning, and full-stack development (Flask for the frontend). It's designed to be simple, scalable, and educational, making it ideal for learning how to combine open-source tools for real-world applications. The source code is available on GitHub, and you can run it locally for testing or demos.

### Key Features
- **URL Input**: User provides a T&C page URL via a minimal web interface.
- **Web Scraping**: Fetches the page content using n8n's HTTP Request node.
- **Data Cleaning**: Removes HTML, CSS, JavaScript, and non-text elements to extract readable text.
- **RAG Summarization**: Uses Retrieval-Augmented Generation to produce a short, plain-language summary.
- **JSON Output**: Returns the summary in JSON format for easy integration.
- **Debugging**: Includes debug fields for troubleshooting URL handling and input.
- **Frontend**: A simple Flask app for user interaction.

### Technologies Used
- **n8n**: For the automation workflow (scraping, processing, and summarization).
- **RAG (Retrieval-Augmented Generation)**: Implemented in Python using libraries like `transformers`, `sentence-transformers`, `faiss`, and `beautifulsoup4`.
- **Flask**: For the web interface to input URLs and display summaries.
- **Python**: For the RAG script (`run_rag.py` and `rag_summarizer.py`).
- **Docker**: (Optional) For running n8n in a containerized environment.
- **GitHub**: For version control and sharing the project.

## How It Works
The system is a backend workflow (n8n) integrated with a frontend interface (Flask). Here's a high-level overview:

1. **User Interaction**: The user opens the Flask app at `http://localhost:5000` and enters a T&C URL (e.g., `https://www.python.org/about/legal/`).
2. **Request to n8n**: Flask sends a GET request to the n8n webhook (`http://localhost:5678/webhook/summarize?url=<USER_URL>`).
3. **n8n Workflow Execution**:
   - The **Webhook** node receives the request and extracts the `url` query parameter.
   - The **Validate URL** node sanitizes and validates the URL, defaulting to a safe URL if invalid.
   - The **HTTP Request2** node fetches the page content using a browser-like User-Agent header to avoid blocking.
   - The **Set** node cleans the scraped HTML, removing tags, scripts, styles, and non-text characters to produce readable text.
   - The **Execute Command** node runs the Python RAG script (`run_rag.py`) to generate the summary.
   - The **Format Output** node extracts the summary from the script's JSON output.
   - The **Respond to Webhook** node returns the summary as JSON (`[{"summary": "<plain-language summary>"}]`).
4. **Response to Flask**: Flask receives the JSON, parses the summary, and displays it in a textarea.
5. **Output**: The user sees a concise summary of the T&C, making it easy to understand without reading the full document.

The workflow is modular, allowing easy extension (e.g., adding email notifications or multi-language support).

## The Science Behind It: Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) is an advanced AI technique that combines retrieval-based methods (searching for relevant information) with generation-based models (like large language models) to produce accurate and context-aware outputs. Here's the science and how it applies to this project:

### Core Concept of RAG
- **Retrieval Phase**: The scraped T&C text is chunked into small segments (e.g., 500 words each). Each chunk is converted into numerical embeddings (vectors) using a model like `all-MiniLM-L6-v2` from `sentence-transformers`. These embeddings are stored in a vector database (FAISS for fast similarity search).
- **Augmentation Phase**: For summarization, a query like "Summarize the key terms and conditions in plain language" is embedded and searched against the vector store to retrieve the top relevant chunks (e.g., top 3 using cosine similarity).
- **Generation Phase**: The retrieved chunks are combined and fed as context to a generative model (e.g., BART from `transformers`), which generates a coherent summary. This ensures the summary is grounded in the actual content, reducing hallucinations (made-up information) common in pure generative models.
- **Advantages**: RAG improves accuracy for long documents like T&C (often 10,000+ words) by focusing on relevant parts, making it efficient and scalable. In this project, it uses Hugging Face models for accessibility and FAISS for fast retrieval, all running locally without cloud dependencies.

### Process in Detail
The project follows a linear pipeline:

1. **Input Reception**:
   - User submits a URL via the Flask form.
   - Flask constructs the webhook URL: `http://localhost:5678/webhook/summarize?url=<USER_URL>`.

2. **Webhook Activation**:
   - n8n's **Webhook** node listens for `GET /summarize`.
   - Extracts the `url` from the query parameters.

3. **URL Validation**:
   - The **Validate URL** node checks if the URL is valid (starts with http/https, no invalid characters).
   - Sanitizes by trimming whitespace and encoding special characters.
   - Defaults to `https://www.python.org/about/legal/` if invalid.
   - Adds `debug_url_input` to log the raw input for troubleshooting.

4. **Web Scraping**:
   - The **HTTP Request2** node fetches the page content as text.
   - Uses a User-Agent header to mimic a browser, avoiding blocks.
   - Timeout and redirect settings handle slow or redirected pages.

5. **Data Cleaning**:
   - The **Set** node removes <script>, <style>, and HTML tags.
   - Normalizes whitespace and removes non-alphanumeric characters (except punctuation).
   - Results in clean, readable text.

6. **RAG Summarization**:
   - The **Execute Command** node runs `run_rag.py` with the cleaned text.
   - `run_rag.py` calls `rag_pipeline` from `rag_summarizer.py`:
     - Cleans the text further using BeautifulSoup.
     - Chunks the text.
     - Creates embeddings and a FAISS index.
     - Retrieves relevant chunks.
     - Generates the summary using BART.
   - Outputs JSON: `{"summary": "<plain-language summary>"}`.

7. **Output Formatting**:
   - The **Format Output** node extracts the `summary` from the JSON.
   - The **Respond to Webhook** node returns `[{"summary": "..."}]`.

8. **Display in Flask**:
   - Flask parses the JSON and shows the summary in a textarea.

This process ensures the summary is accurate, concise, and based on the actual T&C content.

## Installation and Setup
1. **Prerequisites**:
   - Python 3.8+ with libraries: `transformers==4.40.0`, `sentence-transformers==2.7.0`, `faiss-cpu==1.8.0`, `requests==2.31.0`, `beautifulsoup4==4.12.3`, `flask==3.0.3`.
   - n8n running via Docker (as per your setup).
   - GitHub repo cloned.

2. **Setup**:
   - Clone the repo:
     ```
     git clone https://github.com/pranavv1210/Terms-and-Conditions-Summarizer-using-n8n.git
     cd Terms-and-Conditions-Summarizer-using-n8n
     ```
   - Install Python dependencies:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - Start n8n via Docker:
     ```
     docker run -it --rm -p 5678:5678 --network host -v ./tc-scraper-workflow.json:/home/node/tc-scraper-workflow.json n8nio/n8n
     ```
   - Import the workflow in n8n: Workflows > Import from File > Select `tc-scraper-workflow.json`.
   - Activate the workflow (green toggle ON).

3. **Run the Project**:
   - Start the Flask app:
     ```
     python app.py
     ```
   - Open `http://localhost:5000` in your browser.

## Usage
- Enter a T&C URL (e.g., `https://www.python.org/about/legal/`) in the input field.
- Click “Summarize”.
- The summary appears in the textarea below.
- For troubleshooting, check the n8n interface for node outputs or the Flask terminal for logs.

## Visual Representation
The project workflow can be visualized as a linear pipeline:

- User Input (Flask) → Webhook (n8n) → URL Validation → Web Scraping → Data Cleaning → RAG Summarization → Output Formatting → Response to Flask.

For a attractive LinkedIn post, I recommend a diagram showing this flow with icons (e.g., using Canva or Draw.io). 

If you want me to generate a visual representation (e.g., a diagram image of the workflow), can you confirm? Yes or no? If yes, describe any specific style or details (e.g., "colorful flow chart with icons").

## Troubleshooting
- **Invalid URL Error**: Ensure the URL expression in the **HTTP Request2** node is `{{ $node['Validate URL'].json['url'] }}`. Check the `debug_url_input` field in **Validate URL** for input issues.
- **Webhook Not Registered**: Activate the workflow (green toggle ON).
- **No Summary**: Check if `run_rag.py` is at `/home/node/run_rag.py` in Docker. Test `run_rag.py` manually.
- **Scraping Fails**: Try simple URLs; add headers if blocked.
- **Flask Errors**: Check the `n8n response:` log in the Flask terminal for JSON issues.

If issues persist, check n8n logs or share node outputs.

## Credits
- Built by Pranav (pranavv1210)
- Tools: n8n for automation, Hugging Face for RAG models, Flask for the interface.
- Inspiration: xAI's Grok for guidance.

## License
MIT License - Feel free to use and modify for educational purposes.

---