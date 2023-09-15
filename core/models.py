from django.db import models
from django.core.validators import RegexValidator

alpha_validator = RegexValidator(
    regex=r"^[a-zA-Z]*$",
    message="Only alphabets are allowed in the name field.",
    code="invalid_name",
)


class Person(models.Model):
    name = models.CharField(max_length=70, unique=True, validators=[alpha_validator])

    def __str__(self):
        return self.name
