FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mount the cache directory
VOLUME /root/.cache/huggingface

COPY chat.py /
WORKDIR /app
CMD ["streamlit", "run", "--server.port", "8501", "chat.py"]
#docker build -t blendderbodchat .
#docker run -v /Users/dsharma308/.cache/huggingface:/root/.cache/huggingface  -p 8501:8501  blendderbodchat