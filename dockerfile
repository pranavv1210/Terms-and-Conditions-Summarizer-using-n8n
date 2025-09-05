# Use Python 3.10 slim as base (glibc-based for torch compatibility)
FROM python:3.10-slim

# Install Node.js and npm for n8n
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install n8n globally
RUN npm install -g n8n

# Set working directory
WORKDIR /home/node

# Copy project files
COPY run_rag.py /home/node/run_rag.py
COPY rag_summarizer.py /home/node/rag_summarizer.py
COPY requirements.txt /home/node/requirements.txt

# Create and activate virtual environment
RUN python -m venv /home/node/venv
ENV PATH="/home/node/venv/bin:$PATH"

# Upgrade pip to avoid hash issues
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies with force-reinstall
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Create node user and set permissions
RUN useradd -ms /bin/sh node \
    && chown -R node:node /home/node /home/node/venv \
    && chmod +r /home/node/run_rag.py /home/node/rag_summarizer.py

# Switch to node user
USER node

# Expose n8n port
EXPOSE 5678

# Start n8n
CMD ["n8n"]