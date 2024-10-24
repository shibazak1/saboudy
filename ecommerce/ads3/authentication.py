from django.contrib.auth.backends import BaseBackend
from ads3.models import Driver

class DriverBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Driver.objects.get(username=username)
            if user.check_password(password):
                print(f" driver {user}")
                return user
        except Driver.DoesNotExist:
            print("driver does not exists")
            return None

    def get_user(self, user_id):
        try:
            print("Try to find driver by Id")
            return Driver.objects.get(pk=user_id)
        except Driver.DoesNotExist:
            print("there is no driver")
            return None
