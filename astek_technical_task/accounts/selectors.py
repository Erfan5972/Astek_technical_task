from django.contrib.auth import get_user_model


User = get_user_model()

def get_all_users():
    return User.objects.all()