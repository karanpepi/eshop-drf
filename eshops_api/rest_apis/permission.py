from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
from rest_framework.authentication import (get_authorization_header)
from django.utils.encoding import smart_text
from rest_apis.models import Register

class CustomAuthentication(JSONWebTokenAuthentication):


    def get_jwt_value(self, request):
        # import pdb; pdb.set_trace()
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return False

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return False

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_credentials(self,payload):
        # User = get_user_model()
        
        """
        Returns an active user that matches the payload's user id and email.
        """
        username = jwt_get_username_from_payload(payload)
        # import pdb; pdb.set_trace()
        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = Register.objects.get(email=username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        # if not user.is_active:
        #     msg = _('User account is disabled.')
        #     raise exceptions.AuthenticationFailed(msg)

        return user
