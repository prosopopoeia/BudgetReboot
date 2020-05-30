from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import View
#from django.views.generic.detail import DetailView
#from django.views.generic.list import ListView
from .forms import NameForm, AddCatForm
from .models import Category, User, Entry, CatPeriod, AggregateStats, AgStatsPeriod
from django.shortcuts import get_object_or_404, redirect


class indexView(FormView):
    template_name = 'budgetReboot/index.html'
    form_class =  NameForm
          
          
class usertypeView(FormView):
    form_class =  AddCatForm()
    
    def post(self, request):
        v_user_name = request.POST.get('users_name')
        template_name = 'budgetReboot/listcats.html'
        
        try:
            v_user = User.objects.get(users_name = v_user_name)
            
            
        except User.DoesNotExist:
            v_user = User.objects.create(users_name = v_user_name)
            template_name = 'budgetReboot/newuser.html'
            return render(request, template_name, {'form' : self.form_class, 
                                                   'display_user_name' : v_user_name})
        try:
            user_ag_data = AggregateStats.objects.get(owning_user=v_user)            
        except AgStatsPeriod.DoesNotExist:
            user_ag_data = 'unexpected'
            
        try: 
            p_user_ag_data = AgStatsPeriod.objects.get(ag = user_ag_data)
        except AgStatsPeriod.DoesNotExist:
            p_user_ag_data = 'excepted'
       
        
        v_users_categories = Category.objects.filter(owning_user = v_user)
        return render(request, template_name, {'formy' : self.form_class, 
                                                 'display_user_name' : v_user_name, 
                                                 'display_user_cats' : v_users_categories,
                                                 'agstats' : user_ag_data,
                                                 'p_agstats' : p_user_ag_data})
        
class catdetailView(View):
    template_name = 'budgetReboot/catdetail.html'
       
    def post(self, request, h_category_name):
        p_users_name = request.POST.get('h_users_name')
        formage = AddCatForm()       
            
        v_user = get_object_or_404(User, users_name=p_users_name)                   
        v_users_categories = Category.objects.filter(owning_user=v_user)
        v_this_category = v_users_categories.get(category_name=h_category_name)
        v_this_category_this_period = CatPeriod.objects.get(cat=v_this_category)
        v_entry_list = Entry.objects.filter(cat=v_this_category_this_period)
        
        return render(request, self.template_name, {'formy' : formage, 
                                                    'display_user_name' : p_users_name,                                                     
                                                    'display_cat' : v_this_category,
                                                    'display_entries' : v_entry_list,
                                                    'display_cat_period' : v_this_category_this_period})
        

 
class listcatsView(View):
    template_name = 'budgetReboot/listcats.html'
    form_class = AddCatForm()
            
    def post(self, request, p_users_name):
        v_new_category_name = request.POST.get('category_name')
        formage = AddCatForm()       
        v_user = get_object_or_404(User, users_name=p_users_name)   
        
        new_category = Category()
        new_category.category_name = v_new_category_name
        new_category.owning_user = v_user   
        new_category.save();
        
        user_ag_data = AggregateStats.objects.filter(owning_user=v_user)
        p_user_ag_data = AgStatsPeriod.objects.filter(ag = user_ag_data)
        v_users_categories = Category.objects.filter(owning_user=v_user)
        
        return render(request, self.template_name, {'formy' : formage, 
                                                    'display_user_name' : p_users_name, 
                                                    'display_user_cats' : v_users_categories,
                                                    'agstats' : user_ag_data,
                                                    'p_agstats' : p_user_ag_data})       
        
    def get(self, request, pusers_name):
        user_ = User.objects.get(users_name=pusers_name)
        return render(request, template_name, {'display_user_name' : pusers_name})
        
