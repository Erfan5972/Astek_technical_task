import importlib

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Validators پیشنهادی برای فیلدهای مدل:
def validate_running_function(value):
    """
    Validate that the running_function is a valid importable Python path to a callable function.
    Example valid value: 'my_app.tasks.my_task_function'
    """
    try:
        module_path, func_name = value.rsplit('.', 1)
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
    except (ImportError, AttributeError, ValueError) as e:
        raise ValidationError(_("Invalid running function path: %(value)s"), params={'value': value})


def validate_input_schema(value):
    """
    Validate that input_schema is a JSON object with keys as param names and values
    as Python type names (str, int, float, bool).
    Example:
    {
        "param1": "str",
        "param2": "int"
    }
    """
    allowed_types = {"str", "int", "float", "bool"}

    if not isinstance(value, dict):
        raise ValidationError(_("Input schema must be a JSON object (dict)"))

    for key, val_type in value.items():
        if not isinstance(key, str):
            raise ValidationError(_("All keys in input schema must be strings"))
        if val_type not in allowed_types:
            raise ValidationError(_("Invalid type '%(type)s' for key '%(key)s'. Allowed types: %(allowed)s"),
                                  params={'type': val_type, 'key': key, 'allowed': ", ".join(allowed_types)})

