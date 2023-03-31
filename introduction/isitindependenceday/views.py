from django.shortcuts import render
from datetime import datetime


def index(request):
    return render(request, "isitindependenceday/index.html", {
        'is_independence_day': datetime.now().month == 8 and datetime.now().day == 15
    })
