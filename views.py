from django.shortcuts import render
from django.views import generic
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils import timezone
import pathlib

from interface.convert_pdf_to_audio import convert_pdf_to_audio
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
        print(uploaded_file)
        # check if uploaded file in txt using some validation

        print(uploaded_file.size)
        # upload the file onto the created database under the logined user
        fs = FileSystemStorage()
        name = fs.save(phone_number + '/'+uploaded_file.name, uploaded_file)
        print(name)
        first_name = ''
        for c in uploaded_file.name:
            if c != '.':
                first_name += c
            else:
                break
        phone_number = request.user.phone_number
        pathlib.Path('./media/'+phone_number).mkdir(exist_ok=True)
        processing_pages = convert_pdf_to_audio(
            uploaded_file.name, 'media/'+phone_number, 10)
        # output_file = Text_to_speech(uploaded_file.name, first_name)
        request.user.counter -= 1
        request.user.last_use_date = datetime.date.today()
        request.user.save()
        context = {
            "file_name": uploaded_file.name,
            "output_file": 'audio.mp3',
            "url1": fs.url(name),
            "url2": fs.url(phone_number+'/audio.mp3')
        }

    return render(request, 'upload.html', context)