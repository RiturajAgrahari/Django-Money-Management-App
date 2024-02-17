# Django-Money-Management-App
This is my own personal project to learn django.

## Project contains:
* Manage Expenses / Manage Income 
* CRUD operations

## Technologies Used:
* Python
* Django
* Bootstrap
* HTML
* CSS
* JavaScript

## Additional Python Modules Required:
* Django
* Mysql

## Usage:
```
python Django-Money-Management-App/manage.py makemigrations
python Django-Money-Management-App/manage.py migrate
python Django-Money-Management-App/manage.py runserver
```

In your web browser enter the address: http://localhost:8000 or http://127.0.0.1:8000/


## Note:
In your project you have to make sure about these things:

### settings.py:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # or your app_name if any
    'transactions',
    'authentication',
    'user_preferences',
    'userincome',
]
```
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_user_name',
        'PASSWORD': 'your_password',
        'HOST': 'your_host_name',  # localhost --> 127.0.0.1
        'PORT': 'your_port'  # localhost --> 3306
    }
}
```

### urls.py:
```
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions.urls')),
    path('authentication/', include('authentication.urls')),
    path('income/', include('userincome.urls')),
    path('preferences/', include('user_preferences.urls'), name='preference'),
]

```

## Bie...
