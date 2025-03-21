from datetime import datetime
from huey.signals import SIGNAL_EXECUTING, SIGNAL_ERROR, SIGNAL_COMPLETE

from django.db import models
from django.contrib.auth.models import User
from django_huey import get_queue
from polymorphic.models import PolymorphicModel


queue = get_queue("tasks")


class HueyTask(PolymorphicModel):
    """A general-purpose model for handling Huey tasks. It keeps track of a huey task's ID,
    the time created, and the status. Also, this is where we define the functions for handling
    signals sent from the huey consumer.
    """

    huey_id = models.UUIDField(null=True)
    status = models.CharField(max_length=20)
    created = models.DateTimeField(default=datetime.now, blank=True)
    message = models.TextField(default="")

    @classmethod
    @queue.signal(SIGNAL_EXECUTING)
    def start_task(signal, task):
        task_obj = HueyTask.objects.get(huey_id=task.id)
        task_obj.status = "started"
        task_obj.save()

    @classmethod
    @queue.signal(SIGNAL_COMPLETE)
    def end_task(signal, task):
        task_obj = HueyTask.objects.get(huey_id=task.id)
        task_obj.status = "complete"
        task_obj.save()

    @classmethod
    @queue.signal(SIGNAL_ERROR)
    def error_task(signal, task, exc):
        task_obj = HueyTask.objects.get(huey_id=task.id)
        task_obj.status = "error"
        task_obj.message = exc
        task_obj.save()


# ---------------------------------
# Define a singleton model as per
# https://steelkiwi.com/blog/practical-application-singleton-design-pattern/
#
# Then use this to define tables for PrenamingSetting and ClasslistCSV
# ---------------------------------


class SingletonBaseModel(models.Model):
    """We define a singleton models for the test-specification. This
    abstract model ensures that any derived models have at most a single
    row."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class BaseTask(PolymorphicModel):
    """
    A base class for all "tasks" that are sent from the server to
    the PyQT client.

    assigned_user: reference to User, the user currently attached to the task.
                   Can be null, can change over time.
    status: str, represents the status of the task: not started, sent to a client, completed
    """

    # TODO: UUID for indexing
    # TODO: created timestamp
    # TODO: out-of-date boolean field

    assigned_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.TextField(
        null=False, default="todo"
    )  # choices: 'todo', 'out', 'complete'


class BaseAction(PolymorphicModel):
    """
    A base class for all "actions" that pertain to marker user management.
    I.E., grading a question, assigning a task, assigning the task to a new user, etc
    with the goal of saving a "history" of all marking/user management actions.

    user: reference to User, the user who performed the action
    time: datetime, the time the action took place
    task: reference to BaseTask, the task connected to the action
    """

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    task = models.ForeignKey(BaseTask, null=True, on_delete=models.SET_NULL)
