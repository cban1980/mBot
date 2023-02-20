FROM python:3.10.2-slim

WORKDIR /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application
COPY . .

# Start the bot
CMD ["python", "sBot.py"]
