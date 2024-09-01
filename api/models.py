# Author: Sakthi Santhosh
# Created on: 09/01/2023
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

TASK_PRIORITIES = {
    "P0": "High",
    "P1": "Medium",
    "P2": "Low"
}


class Invitee(models.Model):
    first_name = models.CharField(
        max_length=16,
        null=False,
        unique=False,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z]+$",
                message="First name can contain only alphabets.",
                code="invalid_first_name"
            )
        ]
    )
    last_name = models.CharField(
        max_length=16,
        null=False,
        unique=False,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z]+$",
                message="Last name can contain only alphabets.",
                code="invalid_last_name"
            )
        ]
    )
    email = models.EmailField(
        null=False,
        unique=True
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        validators=[
            RegexValidator(
                regex=r"^[\w]+$",
                message="Tags can only contain alphanumeric characters and underscores.",
                code="invalid_tag"
            )
        ]
    )

    def __str__(self):
        return f"#{self.name}"


class TaskGroup(models.Model):
    name = models.CharField(
        max_length=256,
        null=False,
        unique=False
    )
    owner = models.ForeignKey(
        User,
        related_name="task_groups",
        related_query_name="task_group",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "api_task_group"

    def __str__(self):
        return f"{self.name} ({self.owner})"


class Task(models.Model):
    title = models.CharField(
        max_length=256,
        null=False,
        unique=False
    )
    notes = models.TextField(
        null=True,
        unique=False
    )
    related_url = models.URLField(
        null=True,
        unique=False
    )
    reminder = models.DateTimeField(
        null=True,
        unique=False
    )
    location = models.CharField(
        max_length=64,
        null=True,
        unique=False
    )
    flag = models.BooleanField(
        default=False
    )
    priority = models.CharField(
        max_length=2,
        choices=TASK_PRIORITIES,
        null=True,
        unique=False
    )

    task_group = models.ForeignKey(
        TaskGroup,
        related_name="tasks",
        related_query_name="task",
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        related_query_name="task"
    )
    invitees = models.ManyToManyField(
        Invitee,
        related_name="invited_tasks",
        related_query_name="invited_task"
    )

    def __str__(self):
        return f"{self.title}"

    def get_sub_task_list(self):
        return [sub_task["title"] for sub_task in self.sub_tasks.values()]

    def get_tag_list(self):
        return [tag["name"] for tag in self.tags.values()]


class SubTask(models.Model):
    title = models.CharField(
        max_length=256,
        null=False,
        unique=False
    )
    task = models.ForeignKey(
        Task,
        related_name="sub_tasks",
        related_query_name="sub_task",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "api_sub_task"

    def __str__(self):
        return f"{self.title} → {self.task.title}"
