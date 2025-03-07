from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure a username is provided for the superuser
        if not username:
            raise ValueError('Superusers must have a username')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):  # Inherit from PermissionsMixin
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Email is used for login
    REQUIRED_FIELDS = ['username']  # Required fields when creating a user via the admin

    def __str__(self):
        return self.email
