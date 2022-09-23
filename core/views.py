from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import soundfile
from .models import Record
# import speech_recognition as sr
from django.conf import settings
import os
import json
import requests



header = {
	'authorization': '7727ffe82eb44ca79081a199ded9354f',
	'content-type': 'application/json'
}

api_key = '7727ffe82eb44ca79081a199ded9354f'

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload_file(audio_file, header):
    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=_read_file(audio_file)
    )
    return upload_response.json()


def record(request):
    if request.method == "POST":
        try:
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
        except Exception as e:
            f = open('static/log.txt', 'a+')
            f.write('An exceptional thing happed - %s' % e)
            f.close()
    context = {"page_title": "Record audio"}
    return render(request, "core/record.html", context)


def record_detail(request, id):
    record = get_object_or_404(Record, id=id)
    # filename = os.path.join(settings.MEDIA_ROOT, str('new.wav'))
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX : ",filename)
    # out = os.path.join(settings.MEDIA_ROOT, str('out.wav'))
    # data, samplerate = soundfile.read(filename)
    # soundfile.write(out, data, samplerate, subtype='PCM_16')
    # new_file = os.path.join(settings.MEDIA_ROOT, str('out.wav'))

    # # print("HHHHHHHHHHHHHHHHHHHH: ",filename)

    # file = 'logs.txt'
    # # file_ = open(os.path.join(settings.MEDIA_ROOT, file.file.url))
    # f = open(os.path.join(settings.MEDIA_ROOT, file))
    # print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP: ",f.readline())
    # f.close()
    # # filename= r"C:\Users\JO\Downloads\Music\No Excuses Keep Practising Your English Listening Ep 565-d0c58c.mp3"
    # r = sr.Recognizer()

    # # open the file
    # try:
    #     with sr.AudioFile(new_file) as source:
    #         # listen for the data (load audio to memory)
    #         audio_data = r.record(source)
    #         # recognize (convert from speech to text)
    #         text = r.recognize_google(audio_data)
    #         print(text)
    # except:
    #     text = "not Understand"

    filename = os.path.join(settings.MEDIA_ROOT, str(record.voice_record))
    re = upload_file(filename,header)
    file_url = re['upload_url']

    TRANSCRIPT_ENDPOINT = transcript_endpoint

    response = requests.post(
    TRANSCRIPT_ENDPOINT,
    headers={'authorization': api_key, 'content-type': 'application/json'},
    json={
        'audio_url': file_url,
        'sentiment_analysis': True
    },
    )

    response_json = response.json()
    id = response_json['id']

    TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript/'+str(id)

    response = requests.get(
    TRANSCRIPT_ENDPOINT,
    headers={'authorization': api_key},
    )

    response_json_2 = response.json()
    text = response_json['text']




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


def logs(request):
    
    return render(request, "core/index.html",)

