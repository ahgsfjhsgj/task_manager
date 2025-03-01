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

  
