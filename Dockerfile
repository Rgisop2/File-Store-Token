# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Use supported + latest stable base image
FROM python:3.10-slim

# Install git only if your requirements need it (pyrofork needs it sometimes)
RUN apt update && apt install -y git && apt clean

# Copy requirements
COPY requirements.txt /requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r /requirements.txt

# Create working directory
RUN mkdir /VJ-File-Store
WORKDIR /VJ-File-Store

# Copy all project files
COPY . /VJ-File-Store

# Start the bot
CMD ["python3", "bot.py"]
