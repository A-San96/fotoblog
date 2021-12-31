from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'

    def get(self, request):
        return render(request, self.template_name)
