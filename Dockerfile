# 1. Use official Python image
FROM python:3.10-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Install system dependencies for gTTS and audio handling
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy dependency list and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy app files into container
COPY . .

# 6. Expose Streamlit's default port
EXPOSE 8501

# 7. Run Streamlit app
ENTRYPOINT ["streamlit", "run", "dutch_app_streamlit.py", "--server.address=0.0.0.0"]
