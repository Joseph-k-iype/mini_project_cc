#create a model form for cheque data
from django import forms
from .models import upload_cheque
class cheque_form(forms.ModelForm):
    cheque = forms.ImageField()
    class Meta:
        model = upload_cheque
        fields = ['cheque']        