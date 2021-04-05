from django.shortcuts import render
from django.views import generic
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils import timezone

import os
from gtts import gTTS
from gtts import lang
import datetime
# Create your views here.


class HomePageView(generic.TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.last_use_date == datetime.date.today():
                request.user.counter = 5
                request.user.save()
        return super().dispatch(request, *args, **kwargs)


def home(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        if not 'file_name' in request.FILES.keys():
            return render(request, 'index.html')
        uploaded_file = request.FILES['file_name']
        print(uploaded_file.name)
        # check if uploaded file in txt using some validation

        print(uploaded_file.size)
        # upload the file onto the created database under the logined user
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        first_name = ''
        for c in uploaded_file.name:
            if c != '.':
                first_name += c
            else:
                break
        output_file = Text_to_speech(uploaded_file.name, first_name)
        request.user.counter -= 1
        request.user.last_use_date = datetime.date.today()
        request.user.save()
        context = {
            "file_name": uploaded_file.name,
            "output_file": output_file,
            "url1": fs.url(name),
            "url2": fs.url(output_file)
        }

    return render(request, 'upload.html', context)


def Text_to_speech(file_name, first_name):
    input_file = './media/'+file_name
    output_file = './media/'+first_name+".mp3"

    input_text = open(input_file, "r").read().replace("\n", " ")
    language = "en"

    output = gTTS(text=input_text, lang=language, slow=False)
    output.save(output_file)
    # store this file to the database under the logined user
    return first_name+".mp3"
