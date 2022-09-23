from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import soundfile
from .models import Record
import speech_recognition as sr
from django.conf import settings
import os

def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        language = request.POST.get("language")
        record = Record.objects.create(language=language, voice_record=audio_file)
        record.save()
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "url": record.get_absolute_url(),
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}
    return render(request, "core/record.html", context)


def record_detail(request, id):
    record = get_object_or_404(Record, id=id)
    
#     filename = os.path.join(settings.MEDIA_ROOT, str('new.wav'))
    filename = os.path.join(settings.MEDIA_ROOT, str(record.voice_record))
    
#     out = os.path.join(settings.MEDIA_ROOT, str('out.wav'))
#     data, samplerate = soundfile.read(filename)
#     soundfile.write(out, data, samplerate, subtype='PCM_16')
#     new_file = os.path.join(settings.MEDIA_ROOT, str('out.wav'))

    

#     file = 'logs.txt'
#     f = open(os.path.join(settings.MEDIA_ROOT, file))
#     f.close()
    
#     r = sr.Recognizer()

#     # open the file
    try:
        with sr.AudioFile(filename) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            print(text)
    except:
        text = "not Understand"
#     text = "not Understand"

    context = {
        "page_title": "Recorded audio detail",
        "record": record,
        "text": text
    }
    return render(request, "core/record_detail.html", context)


def index(request):
    records = Record.objects.all()
    context = {"page_title": "Voice records", "records": records}
    return render(request, "core/index.html", context)
