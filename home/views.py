from django.shortcuts import render
from django.views import View

class Home(View):
    templates_name = 'home/index.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.templates_name)
