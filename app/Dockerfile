# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py ./
COPY services/ ./services/
COPY static/ ./static/

# Set the default environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Expose the port FastAPI will run on
EXPOSE 8080

# Command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]