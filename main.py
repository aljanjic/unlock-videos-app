
from moviepy.editor import VideoFileClip
import whisper

#audio_file_location = '/app/output/Video_test_1.wav'
audio_file_location2 = '/app/output/Video_test_2.wav'


#video = VideoFileClip("Video_test_1.mp4")
#video.audio.write_audiofile(audio_file_location)

video = VideoFileClip("Video_test_2.mp4")
video.audio.write_audiofile(audio_file_location2)


#  Setting the whisper model parameters size (tiny, base, small, medium, large )
model = whisper.load_model("base")
result = model.transcribe(audio_file_location2)


filename = '/app/output/video_transcript.txt'

with open(filename, 'w') as file:
  file.write(result["text"])

print("text result");
print(result["text"])
print("whole object result")
print(result)


# Analyzer of speech sentiment
# nltk.download('vader_lexicon')

# analyzer = SentimentIntensityAnalyzer()
# scores = analyzer.polarity_scores(text)
# print(scores)

# if scores['compound'] > 0:
#   print('Positive Speech')
# else:
#   print('Negative Speech')