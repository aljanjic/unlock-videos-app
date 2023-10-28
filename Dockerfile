# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Create the /app/output directory and set its permissions
VOLUME /app/output

# Copy your code and video file into the container
COPY Video_test_1.mp4 .
COPY Video_test_2.mp4 .
COPY main.py .

# Install required Python packages for your application
#RUN pip install --no-cache-dir ffmpeg-python moviepy SpeechRecognition nltk openai-whisper

RUN pip install ffmpeg-python moviepy openai-whisper

# Install ffmpeg in the container
RUN apt-get update && apt-get install -y ffmpeg

# Run your script when the container launches
CMD ["python", "main.py"]