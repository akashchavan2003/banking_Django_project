# bank_app/backends.py

from django.contrib.auth.backends import BaseBackend
from .bank_managament_system import authenticate_user

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        
        try:
            authenticated, bank_name = authenticate_user(username, password)
            if authenticated:
                from django.contrib.auth.models import User
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                    user.save()
                return user
        except Exception as e:
            print(f"An error occurred during authentication: {e}")
        
        return None
