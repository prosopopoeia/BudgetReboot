from django.shortcuts import render
from django.views import generic, View
from django.views.generic.edit import FormView
from django.views.generic import FormView
from .forms import NameForm

# Create your views here.


class indexView(generic.FormView):
    template_name = 'budgetReboot/index.html'
    form_class =  NameForm
    success_url = 'budgetReboot/index'
    
   
       
    def form_valid(self, form): 
        # This method is called when valid form data has been POSTed. 
        # It should return an HttpResponse. 
          
        # perform a action here 
        print(form.cleaned_data) 
        return super().form_valid(form) 

        
    # def get_form_class():
         # return NameForm()