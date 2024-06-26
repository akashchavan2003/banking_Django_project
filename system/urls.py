"""
URL configuration for banking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('superuser_login/', views.superuser_login_view, name='superuser_login'),
    path('signup/', views.signup, name='signup'),

    path('home/', views.home_view, name='home'),
    path('debit/', views.debit, name='debit'),
    path('check_ac_bal/', views.check_ac_bal, name='check_ac_bal'),
    path('trf_page/', views.trf, name='trf_page'),
    path('credit/', views.credit, name='credit'), 

    path('fd_account/', views.fd_account, name='fd_account'), 
    path('rd_account/', views.rd_account, name='rd_account'), 
    path('gold_loan/', views.gold_loan, name='gold_loan'), 
    path('fd_loan/', views.fd_loan, name='fd_loan'),  

    path('create_account/',views.create_account,name='create_account'),
    path('fund_fd_account/',views.fund_fd_ac,name='fund_fd_account'), # Add this line
    path('fund_rd_account/',views.fund_rd_ac,name='fund_rd_account') # Add this line
]
