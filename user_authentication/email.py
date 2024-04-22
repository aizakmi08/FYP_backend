# user_authentication/emails.py

from djoser.email import ActivationEmail
from djoser.conf import settings
from django.urls import reverse


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/activation.html'

    def get_context_data(self):
        context = super().get_context_data()

        activation_url = 'http://127.0.0.1:8000/user_authentication/auth/users/activation/' + context['uid'] + '/' + context['token'] + '/'
        context['activation_url'] = activation_url
        print(context['activation_url'])

        return context
