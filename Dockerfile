# Use an updated Python 3.9 slim image
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies (update as necessary for your packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt requirements.txt

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port used by the app
EXPOSE 5002

# Command to run the app
CMD ["python", "run.py"]
