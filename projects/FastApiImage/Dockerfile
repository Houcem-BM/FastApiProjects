# Use a base image with Python installed
FROM python:3.9-slim

# Install required system libraries
RUN apt-get update && apt-get install -y libgomp1

# Copy the FastAPI app and dependencies
WORKDIR /app
COPY AI+api.py /app/AI+api.py
COPY bestModel.pkl /app/bestModel.pkl
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "AI+api:app", "--host", "0.0.0.0", "--port", "8000"]

