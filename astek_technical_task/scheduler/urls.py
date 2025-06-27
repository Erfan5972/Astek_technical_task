from django.urls import path

from astek_technical_task.scheduler.apis import PredefinedTaskListCreateAPI

app_name = 'predefined_tasks'

urlpatterns = [
    path("", PredefinedTaskListCreateAPI.as_view(), name="list_create_predefined_tasks")
]