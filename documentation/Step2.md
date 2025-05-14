# TypeAI

## Second step:

This documentation is for the Second steps to develop in the project for any user of the repo.

## Django Development Guide



### 1. Apps
#### 1.1 Concepts:

- A Django app is a self-contained module within a Django project that handles a specific piece of functionality (e.g., user authentication, blog, or text editing). Apps are reusable and can be plugged into multiple projects.
- An app is a Python package with its own models, views, templates, and URLs. It interacts with the project’s settings and database through Django’s ORM (Object-Relational Mapping). 
- Apps promote modularity, making code easier to maintain, test, and reuse. You can develop an app independently and integrate it into other projects, improving scalability and organization.

#### 1.2 Steps:
1. make the app

``` bash
python TypeAI_djn/manage.py startapp myapp
```
2. Add the app to (`TypeAI_djn/settings.py`):

     ```python
     # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main_feat'
    ]
     # front-end dir setup
     STATIC_URL = '/static/'
     STATICFILES_DIRS = [BASE_DIR / 'static']
     # directing the user to a url (made one in dev)
     LOGIN_REDIRECT_URL = 'dashboard'
     LOGOUT_REDIRECT_URL = 'home'
     ```

3. Run initial migrations to set up the database:
   ```bash
   python manage.py migrate
   ```


2. add to the project

### 2. Models
#### 2.1 Define Models
In `myapp/models.py`, create models for your app.

Conceder Models as tables or classes of objects for entities in your project.

``` python
from django.db import models
# this is an example of a model made by a developer
class MyModel(models.Model):
    # you define the data here with apropriate data types
    name = models.CharField(max_length=100)
    description = models.TextField()
    # the function that displays the string of the object
    def __str__(self):
        # you can edit the form of the output here before returning it
        return self.name
```
#### 2.2 Apply Migrations

To create database tables for your models, run:

``` bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Views

#### 3.1 Create Views

In `myapp/views.py`, define views to handle requests.

``` python
# import the http request library for django, and the models
from django.http import HttpResponse
from .models import MyModel
# make a function that handles the query in models and return the data
def index(request):
    items = MyModel.objects.all()
    return HttpResponse(f"Items: {items}")
```

#### 3.2 Map Views to URLs
In `myapp/urls.py`, define URL patterns.

Note that this is the `urls` for the app not the project

``` python
# import the required django library, and the views you made 
from django.urls import path
from . import views
# use the views in the urlpatterns to path the http request to the url of your choice
urlpatterns = [
    path('', views.index, name='index'),
]
```
### 4. URLs
#### 4.1 Include App URLs
In `myproject/urls.py`, include the URLs of your app.

Note that this is the `urls` for the project not the app
``` python
from django.contrib import admin
from django.urls import path, include
# add the app urls in this format so that the app you made is used in the project
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```
### 5. Migrations
#### 5.1 Make Migrations
After modifying models, create migrations to apply changes.

``` bash
python manage.py makemigrations
```
if you have problems with this command make sure you are in the project directory

#### 5.2 Apply Migrations
Apply migrations to the database.

```bash
python manage.py migrate
```

### 6. Running the Server
#### 6.1 Start the Development Server
```bash
python manage.py runserver
```
Now, open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the project in action.

You can also access the admin page from [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to add or modify data in the database.

---

Make sure to ask questions to your teammates before changing the code they are working on.