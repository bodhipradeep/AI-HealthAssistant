FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port used by FastAPI (uvicorn default 8000)
EXPOSE 8000

# Default command: run uvicorn fastapi_app:app
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
