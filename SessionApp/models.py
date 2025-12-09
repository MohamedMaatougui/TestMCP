from django.db import models
from ConferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

title_validator = RegexValidator(
    regex=r'^[a-zA-Z1-9\s]+$',
    message="only letters and spaces."
)

class Session(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200,blank=True,validators = [title_validator])
    topic = models.CharField(max_length=100)
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if not (self.conference.start_date <= self.session_date <= self.conference.end_date):
            raise ValidationError("La date de la session doit être comprise entre le début et la fin de la conférence.")


        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

    
   