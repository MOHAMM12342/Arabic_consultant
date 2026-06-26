FROM python:3.11-slim

WORKDIR /app

# Install PyTorch with CUDA 12.1 support, then install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8003

# Run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
