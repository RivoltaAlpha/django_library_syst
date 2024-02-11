# authentication_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class RegistrationNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(email=username) 
            if user.check_password(password):
                        logger.info(f"User {user} authenticated successfully")
                        return user
        except UserModel.DoesNotExist:
                    logger.warning(f"User with email={username} not found")
                    return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
