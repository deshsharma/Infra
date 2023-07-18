FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY . .

# Run the code
CMD [ "python", "script.py" ]
#docker build -t my-app .
#docker run my-app