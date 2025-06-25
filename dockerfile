# Use an official Python image
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
