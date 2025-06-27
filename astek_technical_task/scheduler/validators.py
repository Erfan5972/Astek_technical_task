import importlib
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_running_function(value):
    """
    Validate that the running_function is:
    1. A valid Python import path to a callable function.
    2. Located within the HOME_PATH (project base directory).

    Example: 'my_app.tasks.my_task_function'
    """
    try:
        # Ensure it’s a dotted path
        module_path, func_name = value.rsplit('.', 1)

        # Convert dotted module path to file path
        relative_path = os.path.join(*module_path.split('.')) + '.py'

        # Full absolute path
        full_path = os.path.join(settings.HOME_PATH, relative_path)

        # Ensure file exists
        if not os.path.isfile(full_path):
            raise ValidationError(
                _("Python module file does not exist at expected path: %(path)s"),
                params={"path": full_path},
            )

        # Try importing the module and getting the function
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)

        if not callable(func):
            raise ValidationError(
                _("The function '%(func)s' in '%(module)s' is not callable."),
                params={"func": func_name, "module": module_path},
            )

    except (ImportError, AttributeError, ValueError) as e:
        raise ValidationError(
            _("Invalid running function path: %(value)s"),
            params={"value": value}
        )


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

