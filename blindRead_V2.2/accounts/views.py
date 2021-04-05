from django.shortcuts import render
from django.views import generic
from accounts import forms
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
# Create your views here.
class UserSignUpView(generic.CreateView):
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:login')
