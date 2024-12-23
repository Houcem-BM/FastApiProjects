# Use a Python base image
FROM python:3.9-slim

# Install required system libraries
RUN apt-get update && apt-get install -y libgomp1

# Set the working directory
WORKDIR /app

# Copy application files
COPY AI+api.py /app/
COPY requirements.txt /app/
COPY bestModel.pkl /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "AI+api:app", "--host", "0.0.0.0", "--port", "8000"]
