from django.contrib import admin

# Register your models here.

# Okay.

from .models import User, Category, CatPeriod, Entry
admin.site.register(User)
admin.site.register(Category)
admin.site.register(CatPeriod)
admin.site.register(Entry)