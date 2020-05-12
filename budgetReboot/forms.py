from django import forms

class NameForm(forms.Form):
    users_name = forms.CharField(label='Enter User Name', max_length=40)