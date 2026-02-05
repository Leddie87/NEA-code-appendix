from django import forms
from .models import Updatestable

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Updatestable
        fields = ['infoup']
        labels = {
            'infoup': "give updates to all applicants",
        }

