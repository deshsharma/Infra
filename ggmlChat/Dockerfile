#FROM python:3.11
FROM ghcr.io/abetlen/llama-cpp-python:latest
WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install llama-cpp-python==0.1.50 
#COPY /Users/dsharma308/IT7133/models/ggml-vic13b-q5_1.bin /app/ggml-vic13b-q5_1.bin
#--force-reinstall --upgrade --no-cache-dir
COPY . .
COPY chat.py /
WORKDIR /app
CMD ["streamlit", "run", "--server.port", "8501", "chat.py"]