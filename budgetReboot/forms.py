from django import forms

class NameForm(forms.Form):
    users_name = forms.CharField(label='Enter User Name', max_length=40)
    
class AddCatForm(forms.Form):
    category_name = forms.CharField(label='Add New Category', max_length=40)
    