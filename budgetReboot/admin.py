from django.contrib import admin

# Register your models here.

# Okay.

from .models import User, Category, CatPeriod, Entry, AggregateStats, AgStatsPeriod
admin.site.register(User)
admin.site.register(Category)
admin.site.register(CatPeriod)
admin.site.register(Entry)
admin.site.register(AggregateStats)
admin.site.register(AgStatsPeriod)