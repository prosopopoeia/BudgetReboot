from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import NameForm, AddCatForm
from .models import Category, User, Entry, CatPeriod
from django.shortcuts import get_object_or_404


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
            return render(request, template_name, {'form' : self.form_class, 'display_user_name' : v_user_name})
        
        v_users_categories = Category.objects.filter(owning_user = v_user)
        return render(request, template_name, {'form' : self.form_class, 'display_user_name' : v_user_name, 'display_user_cats' : v_users_categories})
        
class catdetailView(FormView):
    template_name = 'budgetReboot/catdetail.html'
    
    def post(self, request, h_category_name):
        p_users_name = request.POST.get('h_users_name')
        formage = AddCatForm()
       
            
        # v_user = get_object_or_404(User, users_name=p_users_name)   
        
        
        # new_category = Category()
        # new_category.category_name = v_new_category_name
        # new_category.owning_user = v_user   
        # new_category.save();
        
        
        #v_users_categories = Category.objects.filter(owning_user=v_user)
        return render(request, self.template_name, {'formy' : formage, 'display_user_name' : p_users_name, 'display_cat_name':h_category_name})
        

 
class listcatsView(FormView):
    template_name = 'budgetReboot/listcats.html'
    form_class = AddCatForm()
    success_url = 'budgetReboot/listcats.html'
    
        
    def post(self, request, p_users_name):
        v_new_category_name = request.POST.get('category_name')
        formage = AddCatForm()
       
        v_user = get_object_or_404(User, users_name=p_users_name)   
        #v_user.save()
        
        new_category = Category()
        new_category.category_name = v_new_category_name
        new_category.owning_user = v_user   
        new_category.save();
        
        
        v_users_categories = Category.objects.filter(owning_user=v_user)
        return render(request, self.template_name, {'formy' : formage, 'display_user_name' : p_users_name, 'display_user_cats' : v_users_categories})
        
        
    def get(self, request, pusers_name):
        user_ = User.objects.get(users_name=pusers_name)
        return render(request, 'budgetReboot/tryme.html', {'display_user_name' : pusers_name})
        
