from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.conf import settings

import mandrill
import logging

import forms


def index2(request):
    return TemplateResponse(request, 'index2.html', {
        'var1': 'This is var1',
        'var2': 'This is var2',
        'list_var': ['a', 'b', 'c'],
    })


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            try:
                # send the contact information via Mandrill
                m = mandrill.Mandrill(settings.MANDRILL_API_KEY)
                m.messages.send({
                    'text': form.cleaned_data.get('message'),
                    'subject': form.cleaned_data.get('subject'),
                    'from_email': form.cleaned_data.get('sender'),
                    'to': [{
                        'email': 'thefatbrat@gmail.com',
                        'name': 'Andy H',
                    }],
                })
                logging.info('Sent contact email: {0}'.format(form.cleaned_data))
            except mandrill.InvalidKeyError, e:
                logging.error('Cannot send contact email: {0}'.format(
                    form.cleaned_data))
                logging.exception(e)
            except mandrill.Error, e:
                logging.error('Cannot send contact email: {0}'.format(
                    form.cleaned_data))
                logging.exception(e)
            return redirect('contact_complete')
    else:
        form = forms.ContactForm()

    return TemplateResponse(request, 'contact.html', {
        'form': form,
    })


def contact_complete(request):
    return TemplateResponse(request, 'contact_complete.html')
