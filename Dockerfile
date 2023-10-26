FROM python:3.9-slim

# Set environment variables for non-interactive (non-tty) operation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

ENV LOG_LEVEL=info

CMD ["python", "dresmon.py"]
