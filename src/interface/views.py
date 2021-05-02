from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.views import generic
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils import timezone
import pathlib
from convert_pdf_to_audio import convert_pdf_to_audio
import os
from gtts import gTTS
from gtts import lang
import datetime
from accounts import models as acct_mdls
# Create your views here.


class HomePageView(generic.TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = acct_mdls.Profile.objects.get(user = request.user)
            if not profile.last_use_date == datetime.date.today():
                profile.counter = 5
                profile.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = None
        if self.request.user.is_authenticated:
            profile = acct_mdls.Profile.objects.get(user = self.request.user)
        if profile:    
            context["counter"] = profile.counter
        return context
    


def upload(request):
    if request.method == 'POST':
        if not 'file_name' in request.FILES.keys():
            return render(request, 'index.html')

        profile = acct_mdls.Profile.objects.get(user = request.user)
        phone_number = profile.mobile
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

        pathlib.Path('./media/'+phone_number).mkdir(exist_ok=True)
        processing_pages = convert_pdf_to_audio(uploaded_file.name, 'media/'+phone_number, profile.counter)
        
        profile.counter -= processing_pages
        profile.last_use_date = datetime.date.today()
        profile.save()
        
        context = {
            "file_name": uploaded_file.name,
            "output_file": 'audio.mp3',
            "url1": fs.url(name),
            "url2": fs.url(phone_number+'/audio.mp3')
        }
        if request.user.is_authenticated:
            profile = acct_mdls.Profile.objects.get(user = request.user)
            context['counter'] = profile.counter
 

    return render(request, 'upload.html', context)



