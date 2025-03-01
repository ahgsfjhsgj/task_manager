
# Task Manager

## Description

A Task Manager project built with Django and MySQL, using Pipenv for virtual environment management.

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python** (latest version)
- **Pipenv** (for managing virtual environments)
- **Django**
- **MySQL Database** (MariaDB latest version)
- **XAMPP** (to manage the database server)

---

## Installation and Setup

### 1. Clone the Repository

```sh
 git clone https://github.com/your-username/task-manager.git
 cd task-manager
```

### 2. Install Pipenv and Dependencies

```sh
pip install pipenv  # If Pipenv is not installed
pipenv install django mysqlclient
```

### 3. Activate the Virtual Environment

```sh
pipenv shell
```

### 4. Configure MySQL Database

- Open **XAMPP** and start the **MariaDB** server.
- Create a new database in MySQL (e.g., `myapp_task`).
- Update `settings.py` in your Django project:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myapp_task',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Create Models in `myapp/models.py`

Define your database models inside `myapp/models.py`. 

```python
from django.db import models
from datetime import date
from django.contrib.auth.models import User
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Update status based on due date
        if self.due_date < date.today():
            self.status = 'OVERDUE'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    default_view = models.CharField(max_length=20, default='all')
    enable_reminders = models.BooleanField(default=False)
    theme = models.CharField(max_length=10, default='light')

    def __str__(self):
        return f"{self.user.username}'s profile"

  

```

### 6. Apply Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the Development Server

```sh
python manage.py runserver
```

Your Task Manager project is now set up and running! 🎉

---


## License

This project is licensed under the MIT License.

