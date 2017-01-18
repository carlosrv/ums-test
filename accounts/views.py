from django.shortcuts import render
from django.shortcuts import render_to_response
import os
import datetime
import crypt
import hashlib

from forms import ContactForm
from models import ProxyAccount
from models import MailAccount
from models import DomainAccount
from models import JabberAccount
from models import Account
from models import AccountsFtpaccount

DOMAIN = "@magcime.cu"

def update_password(username, password, new_password, repeat_password, service):

    if service == "Ftp":
        p = AccountsFtpaccount.objects.filter(ftp_username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.ftp_password == password:
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.ftp_password = new_password
                        ftp_check_password = new_password
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"

    if service == "Internet":
        p = ProxyAccount.objects.filter(proxy_username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.proxy_password == crypt.crypt (password,username):
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.proxy_password = crypt.crypt(new_password,username)
                        user.check_password = crypt.crypt(repeat_password,username)
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"
    elif service == "Internet":
        p = ProxyAccount.objects.filter(proxy_username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.proxy_password == crypt.crypt (password,username):
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.proxy_password = crypt.crypt(new_password,username)
                        user.check_password = crypt.crypt(repeat_password,username)
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"




    elif service == "Correo":
        p = MailAccount.objects.filter(mail_username=username+DOMAIN)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.mail_password == crypt.crypt (password,username):
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.mail_password = crypt.crypt(new_password,username)
                        user.check_password = crypt.crypt(repeat_password,username)
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"

    elif service == "Chat":
        p = JabberAccount.objects.filter(jabber_username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.jabber_password == hashlib.md5(password).hexdigest():
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.jabber_password = hashlib.md5(new_password).hexdigest()
                        user.check_password = hashlib.md5(new_password).hexdigest()
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"

    elif service == "Dominio":
        p = DomainAccount.objects.filter(domain_username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.domain_password == crypt.crypt (password,username):
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.domain_password = crypt.crypt(new_password,username)
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"

    elif service == "Default":
        p = Account.objects.filter(username=username)
        # comprobar que exista usuario
        if p.count() == 1:
            for user in p:
                # comprobar que la contrasena sea correcta
                if user.password == crypt.crypt (password,username):
                    # comprobar que nuevas contrasenas coinciden
                    if new_password == repeat_password:
                        user.password = crypt.crypt(new_password,username)
                        user.check_password= crypt.crypt(new_password,username)
                        user.save()
                        return "Your have changed the password !"
                    else:
                        return "Your must repeat the new password"
                else:
                    return "Invalid password"
        else:
            return "Invalid user"


def password(request):
    information = "Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly."

    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            repeat_password = form.cleaned_data['repeat_password']
            service = form.cleaned_data['service']

            information = update_password(username, password, new_password, repeat_password, service)
            #return HttpResponseRedirect('/thanks/') # Redirect after POST

    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html',  {'form': form, 'information': information})


