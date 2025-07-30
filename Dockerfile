# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all files from your repo into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Optional: expose a port (not required for Telegram bots, but standard)
EXPOSE 8000

# Start the bot
CMD ["python", "bot.py"]
