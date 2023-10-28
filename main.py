# import os
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import ffmpeg
from moviepy.editor import VideoFileClip
import whisper

#audio_file_location = '/app/output/Video_test_1.wav'
audio_file_location2 = '/app/output/Video_test_2.wav'


#video = VideoFileClip("Video_test_1.mp4")
#video.audio.write_audiofile(audio_file_location)

video = VideoFileClip("Video_test_2.mp4")
video.audio.write_audiofile(audio_file_location2)

model = whisper.load_model("base")
result = model.transcribe(audio_file_location2)

# The filename of the file you want to write to
#filename = f'video_transcript.txt'

filename = '/app/output/video_transcript.txt'

with open(filename, 'w') as file:
  file.write(result["text"])

print(result["text"])


# Analyzer of speech sentiment
# nltk.download('vader_lexicon')

# analyzer = SentimentIntensityAnalyzer()
# scores = analyzer.polarity_scores(text)
# print(scores)

# if scores['compound'] > 0:
#   print('Positive Speech')
# else:
#   print('Negative Speech')