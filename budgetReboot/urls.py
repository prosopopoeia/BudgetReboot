"""budgetFantastic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

app_name = 'budgetReboot'
urlpatterns = [
    path('', views.indexView.as_view(), name='index'),
    path('listcats/', views.listcatsView.as_view(), name='listcats'),#tbd tbd remove tbd tbd
    path('usertype/', views.usertypeView.as_view(), name='usertype'),
    path('listcats/<str:p_users_name>', views.listcatsView.as_view(), name='listcats'),
    path('archivelist/<str:h_category_name>', views.archivelistView.as_view(), name='archivelist'),
    path('archivelist/', views.archivelistView.as_view(), name='archivelist'), ###remove TBD TBD TBD TBD
    path('catdetail/<str:h_category_name>', views.catdetailView.as_view(), name='catdetail'),
    path('entryop/<str:h_entry_number>', views.entryopView.as_view(), name='entryop'),
    path('delentry/<int:p_entry_id>', views.delentryView.as_view(), name='delentry'),
]
