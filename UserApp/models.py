import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validateEmail(value):
    allowed_domains = ['esprit.tn', 'univ.tn', 'mit.edu', 'ox.ac.uk']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            f"Email domain '{domain}' is not allowed. Allowed domains are: {', '.join(allowed_domains)}"
        )

name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="This field should contain only alphabetic characters."
)

class User(AbstractUser):
    ROLE_CHOICES = [
        ("participant", "Participant"),
        ("committee", "Organizing Committee Member"),
        ("member", "Member"),
    ]

    user_id = models.CharField(max_length=12,  primary_key=True,unique=True,editable=False)
    email = models.EmailField(unique=True, validators=[validateEmail])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    first_name = models.CharField(max_length=150, blank=True, validators=[name_validator])
    last_name = models.CharField(max_length=150, blank=True, validators=[name_validator])
    affiliation = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_user_id(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=2))
        return f"USER{letters}{numbers}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            new_id = self.generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = self.generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)
