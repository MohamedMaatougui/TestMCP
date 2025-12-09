from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator,FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import random
import string
import datetime
from django.utils import timezone

title_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="only letters and spaces."
)

class Conference(models.Model):
    THEME_CHOICES = [
        ("AI", "Computer Science & Artificial Intelligence"),
        ("SE", "Science & Education"),
        ("SSE", "Social Sciences & Education"),
        ("INT", "Interdisciplinary Themes"),
    ]
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,blank=True, validators=[title_validator])
    theme = models.CharField(max_length=50, choices=THEME_CHOICES)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(validators=[MinLengthValidator(30,"Description must be at least 30 characters long.")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def  clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")




def generate_submission_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=8))
    return f"SUB-{letters}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under_Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    submission_id = models.CharField(
        max_length=12, unique=True, editable=False, blank=True, null=True
    )
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='submissions')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=200)
    abstract = models.TextField(max_length=200)
    key_words = models.CharField(max_length=200)
    paper = models.FileField(
        upload_to='articles/',
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def count_key_words(self):
        if self.key_words:
            mots = self.key_words.split(',')
            if len(mots) > 10:
                raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés.")

    def clean(self):
        errors = {}

        if self.conference and self.submission_date and self.conference.start_date < timezone.now().date():
            errors['conference'] = "La soumission ne peut être faite que pour une conférence à venir."

        if self.author and self.submission_date:
            submissions_today = Submission.objects.filter(
                author=self.author,
                submission_date=self.submission_date
            ).exclude(pk=self.pk).count()
            if submissions_today >= 3:
                errors['author'] = "Vous ne pouvez pas soumettre plus de 3 conférences par jour."

        try:
            self.count_key_words()
        except ValidationError as e:
            errors['key_words'] = e.message

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.submission_id:
            new_id = generate_submission_id()
            while Submission.objects.filter(submission_id=new_id).exists():
                new_id = generate_submission_id()
            self.submission_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submission_id} - {self.title}"
        


class OrganizingCommittee(models.Model):
    COMMITTEE_ROLES = [
        ('chair', 'Chair'),
        ('co-chair', 'Co-Chair'),
        ('member', 'Member'),
    ]

    
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='committee_members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='committee_roles')

    committee_role = models.CharField(max_length=20, choices=COMMITTEE_ROLES)
    date_joined = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)