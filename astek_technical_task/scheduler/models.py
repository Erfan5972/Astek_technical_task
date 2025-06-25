from django_celery_beat.models import PeriodicTask

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from astek_technical_task.scheduler.validators import validate_input_schema, validate_running_function

User = get_user_model()


class PredefinedTask(models.Model):
    """
    Task template defined by admins.
    Each task has a name, description, input schema, and the Python function path to run.
    """
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    input_schema = models.JSONField(
        validators=[validate_input_schema],
        help_text=_("Define expected inputs and their types, e.g. {\"param1\": \"str\", \"param2\": \"int\"}")
    )
    running_function = models.CharField(
        max_length=255,
        validators=[validate_running_function],
        help_text=_("Full Python path to the function to run, e.g., 'my_app.tasks.my_task_function'")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Predefined Task")
        verbose_name_plural = _("Predefined Tasks")
        ordering = ['name']

    def __str__(self):
        return self.name


class UserPeriodicTask(models.Model):
    """
    User-specific scheduled task linking to celery_beat's PeriodicTask.
    Keeps track of which user scheduled which task and if it's active.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("User"))
    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.PROTECT, verbose_name=_("Periodic Task"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("User Periodic Task")
        verbose_name_plural = _("User Periodic Tasks")
        unique_together = ('user', 'periodic_task')

    def __str__(self):
        return f"{self.user.username} - {self.periodic_task.name}"


class TaskExecutionLog(models.Model):
    """
    Logs each execution of a scheduled task.
    Records status, messages, execution time, and links to task and user task.
    """
    STATUS_CHOICES = [
        ("success", _("Success")),
        ("failed", _("Failed"))
    ]

    predefined_task = models.ForeignKey(
        PredefinedTask,
        on_delete=models.CASCADE,
        verbose_name=_("Predefined Task"),
        related_name='execution_logs'
    )
    user_periodic_task = models.ForeignKey(
        UserPeriodicTask,
        on_delete=models.CASCADE,
        verbose_name=_("User Periodic Task"),
        related_name='execution_logs'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name=_("Status"))
    message = models.TextField(verbose_name=_("Message"), blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Executed at"))

    class Meta:
        verbose_name = _("Task Execution Log")
        verbose_name_plural = _("Task Execution Logs")
        ordering = ['-executed_at']

    def __str__(self):
        return f"{self.predefined_task.name} - {self.status} at {self.executed_at.strftime('%Y-%m-%d %H:%M:%S')}"
