import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    userId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=11, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName"]

    def __str__(self):
        return self.email


class Organisation(models.Model):
    orgId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name="organisations")

    def __str__(self):
        return self.name
