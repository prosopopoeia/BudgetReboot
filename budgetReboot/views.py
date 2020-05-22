from django.shortcuts import render
#from django.views import generic, View
from django.views.generic.edit import FormView
#from django.views.generic import FormView
from .forms import NameForm, AddCatForm
from .models import Category, User, Entry, CatPeriod
#from django.views.generic.list import ListView



class indexView(FormView):
    template_name = 'budgetReboot/index.html'
    form_class =  NameForm
    

class listcatsView(FormView):
    template_name = 'budgetReboot/listcats.html'
    form_class = AddCatForm
    success_url = 'budgetReboot/listcats.html'
    
        
    def post(self, request, pusers_name = ''):
        v_user_name = request.POST['users_name']
        formage = AddCatForm()
        try:
            v_user = User.objects.get(users_name = v_user_name)            
        except User.DoesNotExist:
            v_user = User.objects.create(users_name = v_user_name)
        
        v_users_categories = Category.objects.filter(owning_user = v_user)
        return render(request, self.template_name, {'formy' : formage, 'display_user_name' : v_user_name, 'display_user_cats' : v_users_categories})
        
        
    def get(self, request, pusers_name):
        user_ = User.objects.get(users_name=pusers_name)
        return render(request, 'budgetReboot/tryme.html', {'display_user_name' : pusers_name})
        
