from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager as BUM, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from astek_technical_task.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(
            self,
            email: str,
            password: str,
            username: str,
            is_active: bool = True,
            is_admin: bool = False,
            first_name: str = None,
            last_name: str = None
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email.lower()),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin
        )

        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, username: str, first_name: str | None, last_name: str| None):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            is_active=True,
            is_admin=True,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name=_("Username"))
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Last name"))
    email = models.EmailField(unique=True, verbose_name=_("Email address"))

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
