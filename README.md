## 1️⃣ Project structure

```
DutchLearningApp/
│
├── dutch_app_streamlit.py     # Your Streamlit app code
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build instructions
└── README.md
```

---

## 2️⃣ requirements.txt

```txt
streamlit
gtts
requests
BeautifulSoup4
```
---

## 3️⃣ Dockerfile

```dockerfile
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
ENTRYPOINT ["streamlit", "run", "learn_dutch_streamlit.py", "--server.address=0.0.0.0"]
```

---

## 4️⃣ Build the Docker image

From the root directory:

```bash
docker build -t learn-dutch .
```

---

## 5️⃣ Run the container locally

```bash
docker run -p 8501:8501 learn-dutch
```

Then open your browser and go to:

```
http://localhost:8501
```

---

## 6️⃣ Persist progress between runs (optional)

By default, `progress.json` inside the container is **reset** each time.
To keep your learning progress, mount a volume:

```bash
docker run -p 8501:8501 -v $(pwd)/progress.json:/app/progress.json learn-dutch
```

---
