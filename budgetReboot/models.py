from django.db import models
from django.utils import timezone


#                        user
         #                 /    |     \
       # time            jan   feb  dec    etc.
       #                / |                |                                   \
         # categories bank |food  |entertainment| personal care
     #                             /       |             \
    # entries                     entry1  entry2    entry 1   etc. 

#  user1, jan 2020: banking, groceries - user1, feb 2020: banking groceries ...user12 nov 2021: groceries - user 12 dec 2021: groceries...

class User(models.Model):
    users_name = models.CharField(max_length=200)
    
    
class Period(models.Model):
    numeric_month = models.IntegerField(default=0)
    numeric_year = models.IntegerField(default=0)
    
    character_month = models.CharField(default='unknown', max-length = 11)
    character_year = models.CharField(default= 'unknown', max-length = 5)
    
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
class Category(models.Model):
    owningUser = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=200)
    overall_total = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    monthly_total = models.DecimalField(default=0, max_digits=11, decimal_places=2)    
    total_entries = models.IntegerField(default=0)