from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name','theme','location','start_date','end_date','description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
            'description':forms.Textarea(attrs={'rows':4,'cols':40,'placeholder':'Enter a detailed description of the conference'},)
        }