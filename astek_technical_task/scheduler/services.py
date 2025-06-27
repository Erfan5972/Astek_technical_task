from typing import Dict

from rest_framework.exceptions import ValidationError

from astek_technical_task.scheduler.models import PredefinedTask
from astek_technical_task.scheduler.types import PredefinedTaskInterface


def create_predefined_task(interface: PredefinedTaskInterface) -> PredefinedTask:
    """
    Creates a new PredefinedTask instance using model objects directly.

    Args:
        data (dict): Input data for creating a PredefinedTask.

    Returns:
        PredefinedTask: The created task instance.

    Raises:
        ValidationError: If the input data is invalid or missing required fields.
    """
    try:
        task = PredefinedTask.objects.create(
            name=interface.name,
            description=interface.description,
            input_schema=interface.input_schema,
            running_function=interface.running_function,
        )
        return task
    except KeyError as e:
        raise ValidationError(f"Missing required field: {e}")
    except Exception as e:
        raise ValidationError(str(e))