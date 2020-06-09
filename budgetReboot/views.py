from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import View
from django.views.generic.detail import DetailView
#from django.views.generic.list import ListView
from .forms import NameForm, AddCatForm, AddEntryForm, PickArchiveDateForm
from .models import Category, User, Entry, CatPeriod, AggregateStats, AgStatsPeriod
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .utils import eMonth, utils
from django.utils import timezone
import decimal


class indexView(FormView):
    template_name = 'budgetReboot/index.html'
    form_class =  NameForm
          
          
class usertypeView(FormView):
    form_class =  AddCatForm()
    
    def post(self, request):
        v_user_name = request.POST.get('users_name')
        template_name = 'budgetReboot/listcats.html'
        archive_date_form = PickArchiveDateForm()
        
        try:
            v_user = User.objects.get(users_name = v_user_name)
            
            
        except User.DoesNotExist:
            v_user = User.objects.create(users_name = v_user_name)
            v_agstat = AggregateStats.objects.create(owning_user=v_user)
            AgStatsPeriod.objects.create(ag=v_agstat)
            template_name = 'budgetReboot/newuser.html'
            return render(request, template_name, {'form' : self.form_class, 
                                                   'display_user_name' : v_user_name})
        try:
            user_ag_data = AggregateStats.objects.get(owning_user=v_user)            
        except AggregateStats.DoesNotExist:
            return HttpResponseNotFound("AggregateStats, a integral part of the data for a user, is missing")
            
        try: 
            p_user_ag_data = AgStatsPeriod.objects.get(ag = user_ag_data, numeric_month=timezone.now().month, numeric_year=timezone.now().year)
        except AgStatsPeriod.DoesNotExist:
            return HttpResponseNotFound("AggregateStatsPeriod, a integral part of the data for a user, is missing")
       
        
        v_users_categories = Category.objects.filter(owning_user = v_user)
        return render(request, template_name, {'formy' : self.form_class,
                                                 'archiveform' : archive_date_form,
                                                 'display_user_name' : v_user_name, 
                                                 'display_user_cats' : v_users_categories,
                                                 'agstats' : user_ag_data,
                                                 'p_agstats' : p_user_ag_data})
class archivelistView(View):
    template_name = 'budgetReboot/catdetail.html'

    def post(self, request, h_category_name):
        v_archive_mo = request.POST.get('archive_mo')
        v_archive_yr = request.POST.get('archive_yr')
        p_users_name = request.POST.get('h_users_name')
        add_entry_form = AddEntryForm()
        archive_date_form = PickArchiveDateForm()
        v_user = get_object_or_404(User, users_name=p_users_name)   
            
        new_category = get_object_or_404(Category, category_name=h_category_name, owning_user=v_user)        
        
        v_this_category_this_period = get_object_or_404(CatPeriod, 
                                            numeric_month=v_archive_mo, 
                                            numeric_year=v_archive_yr,
                                            cat=new_category)
         
        v_archive_entries = Entry.objects.filter(cat=v_this_category_this_period)                                                
        
        v_users_categories = Category.objects.filter(owning_user=v_user)
        user_ag_data = AggregateStats.objects.filter(owning_user=v_user) ##tbd this should be get
        p_user_ag_data = AgStatsPeriod.objects.filter(ag = user_ag_data) 

        # try:
            # v_cat_avg_all = v_this_category.overall_total / v_this_category.total_entries
        # except Exception as exception:
            # v_cat_avg_all = 666
        try:
            v_cat_avg_month = v_this_category_this_period.monthly_total/ v_this_category_this_period.monthly_entry_count
        except Exception as exception:
            v_cat_avg_month = 777
        
        return render(request, self.template_name, {'formy' : add_entry_form, 
                                                    'archiveform' : archive_date_form,
                                                    'display_user_name' : p_users_name,
                                                    'display_cat' : new_category,
                                                    'display_entries' : v_archive_entries,
                                                    'display_cat_period' : v_this_category_this_period,
                                                    'display_user_cats' : v_users_categories,
                                                    'agstats' : user_ag_data,
                                                    'p_agstats' : p_user_ag_data,
                                                    'month_avg' : round(v_cat_avg_month, 2),
                                                    })   
            
class catdetailView(View):
    template_name = 'budgetReboot/catdetail.html'
       
    def post(self, request, h_category_name):
        p_users_name = request.POST.get('h_users_name')
       
        add_entry_form = AddEntryForm()  #tbd rename form variables     
        archive_date_form = PickArchiveDateForm()
        
        v_user = get_object_or_404(User, users_name=p_users_name)                   
        v_users_categories = Category.objects.filter(owning_user=v_user)
        v_this_category = v_users_categories.get(category_name=h_category_name)
        v_numeric_month = timezone.now().month
        v_numeric_year = timezone.now().year
        v_this_category_this_period = CatPeriod.objects.get(cat=v_this_category, numeric_month=v_numeric_month, numeric_year=v_numeric_year )
        
        try:
            e_amt = request.POST.get('entry_amt')
            e_notes = request.POST.get('entry_notes')
            
            new_entry = Entry()
            new_entry.cat = v_this_category_this_period
            new_entry.entry_note = e_notes
            new_entry.amount = decimal.Decimal(e_amt)
            new_entry.save()   
                        
            v_this_category.overall_total += decimal.Decimal(e_amt)
            v_this_category.total_entries += 1
            v_this_category.save()
            
            try:
                v_agStats = AggregateStats.objects.get(owning_user=v_user)
                v_agStats.grand_total += decimal.Decimal(e_amt)
                v_agStats.save()
            
                v_agStatsPer = AgStatsPeriod.objects.get(ag=v_agStats, numeric_month=timezone.now().month, numeric_year=timezone.now().year)
                v_agStatsPer.month_total += decimal.Decimal(e_amt)
                v_agStatsPer.save()
            except:
                return HttpResponseNotFound("ags didn't save")
            
        except:
            new_entry = ''
            
        if (e_amt):                     
            v_this_category_this_period.monthly_entry_count += 1
            v_this_category_this_period.monthly_total += decimal.Decimal(e_amt)
            v_this_category_this_period.save()
        
            
        v_entry_list = Entry.objects.filter(cat=v_this_category_this_period)
        # try:
            # v_cat_avg_all = v_this_category.overall_total / v_this_category.total_entries
        # except Exception as exception:
            # v_cat_avg_all = 666
        try:
            v_cat_avg_month = v_this_category_this_period.monthly_total/ v_this_category_this_period.monthly_entry_count
        except Exception as exception:
            v_cat_avg_month = 777
        
        return render(request, self.template_name, {'formy' : add_entry_form, 
                                                    'archiveform' : archive_date_form,
                                                    'display_user_name' : p_users_name,                                                     
                                                    'display_cat' : v_this_category,
                                                    'display_entries' : v_entry_list,
                                                    'display_cat_period' : v_this_category_this_period,
                                                    #'all_time_avg' : v_cat_avg_all,
                                                    'month_avg' : v_cat_avg_month})
        
class entryopView(View):
    template_name = 'budgetReboot/entryop.html'
        
    def post(self, request, h_entry_number):
         
        return render(request, self.template_name)
        
        
class delentryView(View):
    template_name = 'budgetReboot/catdetail.html'
        
    def post(self, request, p_entry_id):
        del_entry = Entry.objects.get(id=p_entry_id)
        del_entry_amt = del_entry.amount
        
        del_entry.delete()
        v_users_name = request.POST.get('h_users_name')
        v_category_name = request.POST.get('h_cat_name')
        
        archive_date_form = PickArchiveDateForm()
        add_entry_form = AddEntryForm()       
            
        v_user = get_object_or_404(User, users_name=v_users_name)                   
        v_users_categories = Category.objects.filter(owning_user=v_user)
        
        v_this_category = v_users_categories.get(category_name=v_category_name)
        v_this_category.overall_total -= del_entry_amt
        v_this_category.total_entries -= 1
        v_this_category.save()
                
        v_numeric_month = timezone.now().month
        v_numeric_year = timezone.now().year
                
        v_this_category_this_period = CatPeriod.objects.get(cat=v_this_category, numeric_month=v_numeric_month, numeric_year=v_numeric_year)
        v_this_category_this_period.monthly_total -= del_entry_amt
        v_this_category_this_period.monthly_entry_count -= 1
        v_this_category_this_period.save()
        
        user_ag_data = AggregateStats.objects.get(owning_user=v_user) ##tbd this should be get
        user_ag_data.grand_total -= del_entry_amt
        user_ag_data.save()
        
        p_user_ag_data = AgStatsPeriod.objects.get(ag = user_ag_data, numeric_month=v_numeric_month, numeric_year=v_numeric_year)
        p_user_ag_data.month_total -= del_entry_amt
        p_user_ag_data.save()
        
        v_entry_list = Entry.objects.filter(cat=v_this_category_this_period)                
        
        try:
            v_cat_avg_all = v_this_category.overall_total / v_this_category.total_entries
        except Exception as exception:
            v_cat_avg_all = 0
        try:
            v_cat_avg_month = v_this_category_this_period.monthly_total/ v_this_category_this_period.monthly_entry_count
        except Exception as exception:
            v_cat_avg_month = 0       
        
        return render(request, self.template_name, {'formy' : add_entry_form, 
                                                    'archiveform' : archive_date_form,
                                                    'display_user_name' : v_users_name,                                                     
                                                    'display_cat' : v_this_category,
                                                    'display_entries' : v_entry_list,
                                                    'display_cat_period' : v_this_category_this_period,
                                                    'month_avg' : v_cat_avg_month
                                                    })    

class listcatsView(View):
    template_name = 'budgetReboot/listcats.html'
    #form_class = AddCatForm()
            
    def post(self, request, p_users_name):
        v_new_category_name = request.POST.get('category_name')
        add_cat_form = AddCatForm()        
        v_user = get_object_or_404(User, users_name=p_users_name)   
        
        
        new_category, created_cat = Category.objects.get_or_create(category_name=v_new_category_name, owning_user=v_user)
        # new_category = Category()
        # new_category.category_name = v_new_category_name
        # new_category.owning_user = v_user   
        # new_category.save()
        
        new_cat_period, created_cp = CatPeriod.objects.get_or_create(cat_month=timezone.now().month, 
                                                         cat_year=timezone.now().year,
                                                         cat=new_category)
                                                         
        # new_cat_period = CatPeriod()
        # new_cat_period.cat_month = utils.calculateDayOfMonth(timezone.now().month).name
        # new_cat_period.cat_year = timezone.now().year
        # new_cat_period.cat = new_category
        # new_cat_period.save()        
        
        v_users_categories = Category.objects.filter(owning_user=v_user)
        user_ag_data = AggregateStats.objects.filter(owning_user=v_user) ##tbd this should be get
        p_user_ag_data = AgStatsPeriod.objects.filter(ag = user_ag_data)         
        
        return render(request, self.template_name, {'formy' : add_cat_form,                                                     
                                                    'display_user_name' : p_users_name, 
                                                    'display_user_cats' : v_users_categories,
                                                    'agstats' : user_ag_data,
                                                    'p_agstats' : p_user_ag_data
                                                    })       
    #tbd -> handle redirects, links, whatever    
    def get(self, request, p_users_name):
        v_user = User.objects.get(users_name=p_users_name)
        
        v_users_categories = Category.objects.filter(owning_user=v_user)
        user_ag_data = AggregateStats.objects.get(owning_user=v_user) ##tbd this should be get
        
        v_numeric_month = timezone.now().month
        v_numeric_year = timezone.now().year
        try:
            p_user_ag_data = AgStatsPeriod.objects.get(ag = user_ag_data, numeric_month=v_numeric_month, numeric_year=v_numeric_year)
        except:
            p_user_ag_data = AgStatsPeriod(ag=user_ag_data)
            
        formage = AddCatForm()   #tbd form_class    
        
        return render(request, self.template_name, {'formy' : formage, 
                                                    'display_user_name' : p_users_name, 
                                                    'display_user_cats' : v_users_categories,
                                                    'agstats' : user_ag_data,
                                                    'p_agstats' : p_user_ag_data,
                                                    })       
        
