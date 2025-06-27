from astek_technical_task.scheduler.models import PredefinedTask


def get_all_predefined_tasks() -> list[PredefinedTask]:
    """
    Returns a queryset of all predefined tasks, ordered by name.
    """
    return PredefinedTask.objects.all()