FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Adding sacremoses as requested by the translation pipeline warning
RUN pip install --no-cache-dir -r requirements.txt sacremoses

# Copy application files
COPY . .

# Expose port
EXPOSE 8002

# Run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
