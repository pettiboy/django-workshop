# TODO App with Django

## Setup

-   Install Django using pip

```
pip3 install Django
```

-   Go through the steps of creating a new Django project:

```
django-admin startproject todo_project  # create a number of starter files for our project
cd todo_project                         # navigate into your new project’s directory
python manage.py runserver       # run your server
```

-   Create app

```
python manage.py startapp todo
```

-   Add `todo` to `INSTALLED_APPS` list in `settings.py`

## Creating Index View

-   In your project's urls.py at `todo_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include("todo.urls"))
]
```

-   Create a new `urls.py` file in your app (the `todo` folder)

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index")
]
```

-   In your `views.py`

```python
from django.shortcuts import render, redirect

def index(request):
    todos = ["lorem", "ipsum", "dolor"]
    return render(request, "todo/index.html" , {
        "todos": todos
    })
```

-   Create new folder `templates/todo` and create a file `index.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Todos</title>
    </head>
    <body>
        <ul>
        {% for todo in todos %}
            <li>{{ todo }}</li>
        {% endfor %}
        </ul>
    </body>
</html>
```

-   We also need to know if a particular todo is completed or not so we store it in a dictionary

```python
def index(request):
    todos = [
        {
            "title": "lorem",
            "is_completed": False
        },
        {
            "title": "ipsum",
            "is_completed": True
        },
        {
            "title": "dolor",
            "is_completed": False
        }
    ]
    return render(request, "todo/index.html" , {
        "todos": todos
    })
```

-   concept of list of dictionary in above snippet

    -   `todos` is a list of dictionaries
    -   each dictionary has two keys `title` and `is_completed`
    -   `title` is a string
    -   `is_completed` is a boolean

-   We update the `index.html` file to reflect the changes

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Todos</title>
    </head>
    <body>
        <ul>
        {% for todo in todos %}
            <li>
                <span class="title">{{ todo.title }} -- </span>
                {% if todo.is_completed %}
                    <span class="completed">Completed</span>
                {% else %}
                    <span class="not-completed">Not Completed</span>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    </body>
</html>
```

## Storing Todos in Database

-   We need to create a model for our todos

```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
```

-   We need to tell Django that we have made changes to our model

```
python manage.py makemigrations
```

-   We need to apply the changes to our database

```
python manage.py migrate
```

## Django Admin Panel

-   We need to register our model in `admin.py`

```python
from django.contrib import admin
from .models import Todo

admin.site.register(Todo)
```

-   We need to create a superuser to access the admin panel

```
python manage.py createsuperuser
```

-   We will browse the Todo model in the admin panel at `http://localhost:8000/admin/`

-   Observations and concepts for django admin panel

    -   we see user and group models
    -   we see a list of todos
    -   we can create a new todo
    -   we can edit a todo
    -   we can delete a todo

## Fetching Todos from Database

-   We need to update our `index` view to fetch todos from the database

```python
from django.shortcuts import render, redirect
from .models import Todo

def index(request):
    todos = Todo.objects.all()
    return render(request, "todo/index.html" , {
        "todos": todos
    })
```

-   We see that the todos we added in admin panel are now displayed in our index view

## Creating Todos

-   Lets start by creating a form in our `index.html` file

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Todos</title>
    </head>
    <body>
        <form action="{% url 'create' %}" method="POST">
            {% csrf_token %}
            <input type="text" name="title" placeholder="Enter todo title">
            <button type="submit">Create</button>
        </form>
        <ul>
        {% for todo in todos %}
            <li>
                <span class="title">{{ todo.title }} -- </span>
                {% if todo.is_completed %}
                    <span class="completed">Completed</span>
                {% else %}
                    <span class="not-completed">Not Completed</span>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    </body>
</html>
```

-   concepts to understand in the above form snippet

    -   `action="{% url 'create' %}"` - this is the url that the form will be submitted to
    -   `method="POST"` - this is the method that the form will be submitted with
    -   `{% csrf_token %}` - this is a security token that Django requires to be present in all forms
    -   `name="title"` - this is the name of the input field

-   Now lets create a view to handle the creation of todos

-   We need to create a new url for the new view

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create")
]
```

-   We write a new view to handle the creation of todos

```python
def create(request):
    title = request.POST["title"]
    Todo.objects.create(title=title)
    return redirect("index")
```

## Toggling Todos Completion

-   We update index.html to add a button to toggle the completion of a todo

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Todos</title>
    </head>
    <body>
        <form action="{% url 'create' %}" method="POST">
            {% csrf_token %}
            <input type="text" name="title" placeholder="Enter todo title">
            <button type="submit">Create</button>
        </form>
        <ul>
        {% for todo in todos %}
            <li>
                <span class="title">{{ todo.title }} -- </span>
                {% if todo.is_completed %}
                    <span class="completed">Completed</span>
                {% else %}
                    <span class="not-completed">Not Completed</span>
                {% endif %}
                <form action="{% url 'toggle' todo.id %}" method="POST">
                    {% csrf_token %}
                    <button type="submit">Toggle</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    </body>
</html>
```

-   concepts to understand in the above form snippet

    -   todo object also contains an id field which is a primary key
    -   we use the id field to create a url for the toggle view
    -   this id field is given by default to every model by django

-   We need to create a new url for the new view

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("toggle/<int:todo_id>/", views.toggle, name="toggle")
]
```

-   We write a new view to handle the toggling of todos

```python
def toggle(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("index")
```

-   concepts to understand in the above view

    -   we get the `todo` object from the database using the id
    -   we toggle the `is_completed` field
    -   we `save` the todo object to the database

## Deleting Todos

-   We update index.html to add a button to delete a todo

<!-- prettier-ignore -->
```html
<!DOCTYPE html>

<html lang="en">
    <head>
        <title>Todos</title>
    </head>
    <body>
        <form action="{% url 'create' %}" method="POST">
            {% csrf_token %}
            <input type="text" name="title" placeholder="Enter todo title">
            <button type="submit">Create</button>
        </form>
        <ul>
        {% for todo in todos %}
            <li>
                <span class="title">{{ todo.title }} -- </span>
                {% if todo.is_completed %}
                    <span class="completed">Completed</span>
                {% else %}
                    <span class="not-completed">Not Completed</span>
                {% endif %}
                <form action="{% url 'toggle' todo.id %}" method="POST">
                    {% csrf_token %}
                    <button type="submit">Toggle</button>
                </form>
                <form action="{% url 'delete' todo.id %}" method="POST">
                    {% csrf_token %}
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    </body>
</html>
```

-   We need to create a new url for the new view

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("toggle/<int:todo_id>/", views.toggle, name="toggle"),
    path("delete/<int:todo_id>/", views.delete, name="delete")
]
```

-   We write a new view to handle the deletion of todos

```python
def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect("index")
```

-   concepts to understand in the above view

    -   we get the `todo` object from the database using the id
    -   we `delete` the todo object from the database

## Styling the Todo App

-   We use Bootstrap 5 to style the todo app

-   We add the following to the head of index.html

<!-- prettier-ignore -->
```html
 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
```

-   just before the closing body tag of index.html

<!-- prettier-ignore -->
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N" crossorigin="anonymous"></script>
```

-   We add the following to `index.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>

<html lang="en">
    <head>
        <title>Todos</title>
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp"
            crossorigin="anonymous"
        />
    </head>

    <body>
        <div class="container mt-5">
            <h1>Todo List</h1>
            <form action="{% url 'create' %}" method="POST" class="mb-3">
                {% csrf_token %}
                <div class="input-group">
                    <input
                        type="text"
                        name="title"
                        placeholder="Enter todo title"
                        class="form-control"
                    />
                    <button type="submit" class="btn btn-primary">
                        Create
                    </button>
                </div>
            </form>

            <ul class="list-group">
                {% for todo in todos %}
                <li
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                    <span class="title">{{ todo.title }}</span>
                    <span
                        class="badge {% if todo.is_completed %}bg-success{% else %}bg-danger{% endif %}"
                    >
                        {% if todo.is_completed %} 
                            Completed 
                        {% else %} 
                            Not Completed 
                        {% endif %}
                    </span>
                    <div>
                        <form
                            action="{% url 'toggle' todo.id %}"
                            method="POST"
                            class="d-inline"
                        >
                            {% csrf_token %}
                            <button
                                type="submit"
                                class="btn btn-sm btn-secondary"
                            >
                                Toggle
                            </button>
                        </form>
                        <form
                            action="{% url 'delete' todo.id %}"
                            method="POST"
                            class="d-inline"
                        >
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-danger">
                                Delete
                            </button>
                        </form>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>

        <script
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-qKXV1j0HvMUeCBQ+QVp7JcfGl760yU08IQ+GpUo5hlbpg51QRiuqHAJz8+BrxE/N"
            crossorigin="anonymous"
        ></script>
    </body>
</html>
```

-   Understanding `classes` in the above snippet with bootstrap documentation for the same.

    -   `container` class
        -   https://getbootstrap.com/docs/5.0/layout/containers/
    -   `mt-5` class
        -   https://getbootstrap.com/docs/5.0/utilities/spacing/
    -   `form-control` class
        -   https://getbootstrap.com/docs/5.0/forms/form-control/
    -   `btn` class
        -   https://getbootstrap.com/docs/5.0/components/buttons/
    -   `list-group` class
        -   https://getbootstrap.com/docs/5.0/components/list-group/
    -   `d-flex` class
        -   https://getbootstrap.com/docs/5.0/utilities/flex/
    -   `justify-content-between` class
        -   https://getbootstrap.com/docs/5.0/utilities/flex/#justify-content
    -   `align-items-center` class
        -   https://getbootstrap.com/docs/5.0/utilities/flex/#align-items
    -   `badge` class
        -   https://getbootstrap.com/docs/5.0/components/badge/
    -   `bg-success` class
        -   https://getbootstrap.com/docs/5.0/utilities/colors/#background-color
    -   `bg-danger` class
        -   https://getbootstrap.com/docs/5.0/utilities/colors/#background-color
    -   `btn-sm` class
        -   https://getbootstrap.com/docs/5.0/components/buttons/#sizes
    -   `btn-secondary` class
        -   https://getbootstrap.com/docs/5.0/components/buttons/#examples
    -   `btn-danger` class
        -   https://getbootstrap.com/docs/5.0/components/buttons/#examples
