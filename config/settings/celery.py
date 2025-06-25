import os

# URL of the message broker that Celery will use to send and receive messages.
# Typically Redis or RabbitMQ. Here, it uses the REDIS_URL environment variable,
# falling back to localhost Redis if not set.
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Backend used to store task results.
# Often the same as the broker (Redis in this case), but can be different.
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Specifies the scheduler class for celery-beat.
# This setting enables django-celery-beat to store periodic task schedules in the Django database.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Content types Celery will accept. Here, only JSON format is accepted.
CELERY_ACCEPT_CONTENT = ['json']

# Serializer used to serialize task arguments when sending tasks to workers.
CELERY_TASK_SERIALIZER = 'json'

# Serializer used to serialize task results when storing them in the backend.
CELERY_RESULT_SERIALIZER = 'json'

# Logging level for Celery workers.
# INFO level provides general operational information without too much verbosity.
CELERYD_LOG_LEVEL = 'INFO'
