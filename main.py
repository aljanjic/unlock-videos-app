# import os
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import ffmpeg
from moviepy.editor import VideoFileClip
from speech_recognition import Recognizer, AudioFile
# Not needed for now: 
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer


recognizer = Recognizer()

audio_file_location = '/app/output/Video_test_1.wav'

video = VideoFileClip("Video_test_1.mp4")
video.audio.write_audiofile(audio_file_location)

with AudioFile(audio_file_location) as audio_file:
  audio = recognizer.record(audio_file)

text = recognizer.recognize_google(audio)

# The filename of the file you want to write to
#filename = f'video_transcript.txt'

filename = '/app/output/video_transcript.txt'


# Open the file with writing permission
with open(filename, 'w') as file:
  # Write text to the file
  file.write(text)

print(text)



# Analyzer of speech sentiment
# nltk.download('vader_lexicon')

# analyzer = SentimentIntensityAnalyzer()
# scores = analyzer.polarity_scores(text)
# print(scores)

# if scores['compound'] > 0:
#   print('Positive Speech')
# else:
#   print('Negative Speech')