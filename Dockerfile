# Use an official Python runtime as a parent image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Create the /app/output directory and set its permissions
VOLUME /app/output

# Copy your code and video file into the container
COPY Test_videos/Video_test_1.mp4 .
COPY main.py .

# Install ffmpeg, build tools, C++ compiler, and OpenBLAS in the container
RUN apk add --no-cache ffmpeg flac gcc g++ musl-dev python3-dev openblas-dev

# Install required Python packages for your application
RUN pip install --no-cache-dir ffmpeg-python moviepy SpeechRecognition nltk

# Run your script when the container launches
CMD ["python", "main.py"]
