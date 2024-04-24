from django.urls import reverse
from djoser.email import ActivationEmail


class CustomActivationEmail(ActivationEmail):
    template_name = 'email/activation_email.html'

    def get_context_data(self):
        context = super().get_context_data()
        uid = context['uid']
        token = context['token']

        # Construct the activation URL
        activation_url = reverse('user_activation', kwargs={'uid': uid, 'token': token})

        # Combine activation URL with the context
        context['activation_url'] = activation_url

        return context
