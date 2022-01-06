from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms


class SignupPageView(View):
    form_class = forms.SignupForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})


class UploadProfilePhotoView(LoginRequiredMixin, View):
    form_class = forms.UploadProfilePhotoForm
    template_name = 'authentication/upload_profile_photo.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            photo = form.save(commit=False)
            # now we can save
            photo.save()
            return redirect('home')

        return render(request, self.template_name, context={'form': form})
