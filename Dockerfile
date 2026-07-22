FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    fonts-dejavu-core \\
    fonts-liberation \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

ENV PORT=10000

CMD ["python", "bot.py"]