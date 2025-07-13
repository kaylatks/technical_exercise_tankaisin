# Use an official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy all files from SectionB into /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your main script by default
CMD ["python", "main.py"]
