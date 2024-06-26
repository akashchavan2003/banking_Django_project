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
from django.contrib import admin
from django.urls import path, include
from system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.empty_login_view, name='empty_login'),  # Set login.html as the default landing page
    path('system/', include('system.urls')),  # Include system app URLs (if necessary)
    path('signup/', views.signup, name='signup'),  # URL for signup form
    path('login/', views.login_view, name='login'),  # URL for regular user login
    path('check_ac_bal/', views.check_ac_bal, name='check_ac_bal'),
    path('trf_page/', views.trf, name='trf'),
    path('credit/', views.credit, name='credit'),
    path('debit/', views.debit, name='debit'),
    path('create_account/',views.create_account,name='create_account'), 
    path('fd_account/', views.fd_account, name='fd_account'), 
    path('rd_account/', views.rd_account, name='rd_account'), 
    path('gold_loan/', views.gold_loan, name='gold_loan'), 
    # path('form2/', views.form2, name='form2'),  
    path('fd_loan/', views.fd_loan, name='fd_loan'), 
    path('fund_fd_account/',views.fund_fd_ac,name='fund_fd_account'), # Add this line
    path('fund_rd_account/',views.fund_rd_ac,name='fund_rd_account'), # Add this line
    path("__debug__/", include("debug_toolbar.urls")),
]   
