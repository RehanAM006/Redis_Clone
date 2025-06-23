# Use official Python slim image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

RUN pip install --no-cache-dir --upgrade pip

# Set default command to run your server
CMD ["python", "server.py"]

