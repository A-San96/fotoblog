from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms, models


class HomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'
    photo_class = models.Photo
    blog_class = models.Blog

    def get(self, request):
        photos = self.photo_class.objects.all()
        blogs = self.blog_class.objects.all()
        return render(request, self.template_name, context={'photos': photos, 'blogs': blogs})


class PhotoUploadView(LoginRequiredMixin, View):
    form_class = forms.PhotoForm
    template_name = 'blog/photo_upload.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')

        return render(request, self.template_name, context={'form': form})


class BlogAndPhotoUploadView(LoginRequiredMixin, View):
    blog_form_class = forms.BlogForm
    photo_form_class = forms.PhotoForm
    template_name = 'blog/create_blog_post.html'

    def get(self, request):
        blog_form = self.blog_form_class()
        photo_form = self.photo_form_class()
        context = {
            'blog_form': blog_form,
            'photo_form': photo_form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        blog_form = self.blog_form_class(request.POST)
        photo_form = self.photo_form_class(request.POST, request.FILES)

        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save()
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('home')

        context = {
            'blog_form': blog_form,
            'photo_form': photo_form
        }
        return render(request, self.template_name, context=context)


class BlogView(LoginRequiredMixin, View):
    template_name = 'blog/view_blog.html'

    def get(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        return render(request, self.template_name, context={'blog': blog})
