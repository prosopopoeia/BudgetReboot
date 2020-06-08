from django import forms
import datetime

class NameForm(forms.Form):
    users_name = forms.CharField(label='Enter User Name', max_length=40)
    
class AddCatForm(forms.Form):
    category_name = forms.CharField(label='Add New Category', max_length=40)
    
class AddEntryForm(forms.Form):
    entry_amt = forms.DecimalField(max_digits=11, decimal_places=2, label="Entry amount")
    entry_notes = forms.CharField(max_length=100, label="Entry notes")
    
class PickArchiveDateForm(forms.Form):
    #archive_date = forms.DateField(initial=datetime.date.today, label = "Format: yyyy-mm-dd-")
    archive_mo = forms.IntegerField(label = "Enter Numeric Month")
    archive_yr = forms.IntegerField(label = "Enter Numeric Year")