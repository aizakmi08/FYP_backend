from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from djoser import signals


class UserActivationView(View):
    @staticmethod
    def post(request, uid, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and user.activation_token == token:
            user.is_active = True
            user.save()
            signals.user_activated.send(sender=User, user=user, request=request)
            # Redirect to a success page or wherever you want
            return redirect('activation_success')
        else:
            # Handle invalid activation link
            return redirect('activation_failure')
