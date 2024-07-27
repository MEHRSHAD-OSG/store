

from django.core.exceptions import ValidationError
from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin

def send_otp_code(phone_number,code):
    try:

        api = KavenegarAPI('766D374A566B32355A44377758564A514D734738684157634963487146626B61784A3061727075683874733D')
        params = {'sender': '', 'receptor': phone_number, 'message': f'{code} کد تایید '}
        response = api.sms_send(params)
        print('='*90)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)



class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
