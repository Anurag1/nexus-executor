# Dockerfile
FROM nvidia/cuda:12.1-base-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install Node dependencies for frontend
RUN cd interfaces/chatbot/static && \
    npm install

# Expose ports
EXPOSE 8000  # FastAPI
EXPOSE 8080  # Frontend

# Create volumes for persistent data
VOLUME ["/app/data", "/app/models", "/app/logs"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["sh", "-c", "uvicorn interfaces.chatbot.main:app --host 0.0.0.0 --port 8000 & \
     cd interfaces/chatbot && python3 -m http.server 8080"]
