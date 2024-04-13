FROM python:latest

# Set working directory in the container
WORKDIR /app

# Copy requirements and script files into the container
COPY requirements.txt .
COPY readOpcData.py .
COPY config.json .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONUNBUFFERED environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the script
CMD ["python", "readOpcData.py"]
