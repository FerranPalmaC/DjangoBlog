from members.models import CustomUser
from django.contrib.auth.backends import ModelBackend

class EmailAuthenticationBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(self, request, username, password):
        user_email = username 
        password = password 
        try:
            user = CustomUser.objects.get(email=user_email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
