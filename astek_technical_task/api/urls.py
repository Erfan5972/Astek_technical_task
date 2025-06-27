from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('accounts/', include('astek_technical_task.accounts.urls', namespace='accounts')),
    path('predefined_tasks/', include('astek_technical_task.scheduler.urls', namespace='predefined_tasks'))
]
