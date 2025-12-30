from django.db import models
from django.conf import settings
from rooms.models import Room

class HousekeepingTask(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="housekeeping_tasks")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="tasks"
    )
    task_description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Task for {self.room.room_number}: {self.status}"
