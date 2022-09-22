# import speech_recognition as sr

filename= "C:\\Users\\JO\\Downloads\\Music\\No Excuses Keep Practising Your English Listening Ep 565-d0c58c.mp3"
filename_2= "C:\\Users\\JO\\Downloads\\Music\\fgfffgfgf.mp3"

# r = sr.Recognizer()

# # open the file
# with sr.AudioFile(filename) as source:
#     # listen for the data (load audio to memory)
#     audio_data = r.record(source)
#     # recognize (convert from speech to text)
#     text = r.recognize_google(audio_data)
#     print(text)

import pydub 
sound = pydub.AudioSegment.from_wav(filename) 
sound.export(filename_2, format="mp3")