from django.db import models
from django.utils import timezone

      #                        user
         #                 /    |     \
       #                   categories bank |food  |entertainment| personal care
       #                / |                |                                   \
         #            period    jan   feb  dec     (...+year)   etc.
     #                             /       |             \
    # entries                     entry1  entry2    entry 1   etc. 

#  user1, jan 2020: banking, groceries - user1, feb 2020: banking groceries ...user12 nov 2021: groceries - user 12 dec 2021: groceries...

class User(models.Model):
    users_name = models.CharField(max_length=200)    


class Category(models.Model):
    owning_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=200)    
    
    overall_total = models.DecimalField(default=0, max_digits=11,  decimal_places=2)
    total_entries = models.IntegerField(default=0)


    
class CatPeriod(models.Model):
    numeric_month = models.IntegerField(default=timezone.now().month)
    numeric_year = models.IntegerField(default=timezone.now().year)
    
    def is_current_month(self):
        this_moment = timezone.now().month
        return numeric_month ==  transaction_date.month
    
    cat_month = models.CharField(max_length = 11)
    cat_year = models.CharField(max_length = 5)
    
    monthly_total = models.DecimalField(default=0, max_digits=11, decimal_places=2)    
    monthly_entry_count = models.IntegerField(default=0)
        
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
        
    
class Entry(models.Model):
    cat = models.ForeignKey(CatPeriod, on_delete=models.CASCADE)
    entry_note = models.CharField(default='', max_length=11)
    source = models.CharField(default='', max_length=25)
    amount = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    transaction_date=models.DateTimeField('transaction date',default=timezone.now, blank=True)
    
    def is_current_month(self):
        this_moment = timezone.now().month
        return this_moment ==  transaction_date.month
    
    def __str__(self):
        return self.entry_note

class AggregateStats(models.Model):
    owning_user = models.ForeignKey(User, on_delete=models.CASCADE)
    grand_total = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    avg_monthly_expeditures = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    grand_income = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    avg_monthly_income  = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    number_of_months = models.IntegerField(default=0)
    
    
class AgStatsPeriod(models.Model):
    ag = models.ForeignKey(AggregateStats, on_delete=models.CASCADE)
    
    numeric_month = models.IntegerField(default=timezone.now().month)
    numeric_year = models.IntegerField(default=timezone.now().year)
    
    month_total = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    month_income = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    
    