from django.shortcuts import render, redirect
from .models import Todo


def index(request):
    todos = Todo.objects.all()
    return render(request, "todo/index.html", {
        "todos": todos
    })


def create(request):
    title = request.POST["title"]
    Todo.objects.create(title=title)
    return redirect("index")


def toggle(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("index")
