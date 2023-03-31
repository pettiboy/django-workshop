from django.shortcuts import HttpResponse, render


def index(request):
    return render(request, "hello/index.html")


def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })
