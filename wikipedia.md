# Create wikipedia project
django-admin startproject wikipedia

# Create wikipedia app
python manage.py startapp wiki_app

# Put wiki_app in settings.py of wikipedia
    INSTALLED_APPS = [
        'wiki_app',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

# Write Model in 'models.py' of wiki_app
    from django.db import models
    class WikiModel (models.Model):
        title = models.CharField(primary_key=True , max_length=50)
        content=models.TextField(max_length=50)

# Register Model in 'admin.py' of wiki_app
    from django.contrib import admin
    from .models import WikiModel
    admin.site.register(WikiModel)

# Make Migrations (follow order)
    python manage.py makemigrations
    python manage.py migrate

# urls.py
    from django.urls import path
    from . import views
    urlpatterns = [
        path("",views.index, name="index"),
        path("add",views.add, name="add"),
        path("wiki",views.wiki, name="wiki"),
    ]

# views.py
    from django import forms
    from django.shortcuts import render
    from django.http import HttpResponse , HttpResponseRedirect
    from django.urls import reverse
    from .models import WikiModel

    def index(request):
        return HttpResponse('Hi')

    class WikiForm(forms.Form):
        title=forms.CharField(label='Page Title',min_length=5)
        content=forms.CharField(widget=forms.Textarea(),label='Your Content')

    def wiki(request):
        data = WikiModel.objects.all()
        return render(request, "wiki.html", {
            'wiki_data':data
        })

    def add(request):
        if request.method == "POST":
            form = WikiForm(request.POST)
            if(form.is_valid()):
                title  = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                data  = WikiModel(title, content)
                data.save()
                return HttpResponseRedirect(reverse('wiki'))
        return render(request, "add.html", {
            "form":WikiForm()
        })
