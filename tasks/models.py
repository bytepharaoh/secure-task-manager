from django.db import models
from django.contrib.auth.models import User


class Task (models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ]
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description=models.TextField(blank=True )
    completed= models.BooleanField(default=False)
    priority=models.CharField(max_length=10 ,choices=PRIORITY_CHOICES , default='medium')
    created_at=models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True , blank= True)

    def __str__(self):
        if self.due_date:
            return (f"ID: {self.id}: Title {self.title} Created at  {self.created_at} Due to {self.due_date}")
        else:
            return f"ID: {self.id}: Title {self.title} Created at {self.created_at}"

    def priority_order(self):
        """Return numeric value for sorting (higher = more important)"""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        return priority_map.get(self.priority, 0)
