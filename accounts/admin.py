from django.contrib import admin

# Register your models here.
# Django admin.py for ums project.

##################################
DEBUG = 0
ALL_VIEWS = 0
DOMAIN = "magcime.cu"
pdcHost = '10.36.2.100'
pdcPort = 50007
##################################

from .models import Account
from .models import AccountsFtpaccount
from .models import Department
from .models import Area
from .models import ProxyAccount
from .models import MailAccount
from .models import MailAlias
from .models import DomainAccount
from .models import JabberAccount
from .models import ProxyQuotaType
from .models import ProxyAccountType
from .models import MailAccountType
from .models import DomainGroupType
from django.contrib import admin
from django import forms
import crypt, hashlib
import os
#import win_crypt as crypt
import sys
from socket import *


# Poner los passwords en forma de passwords_input(*******), y crea los campos del form
class InlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
#            'ftp_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
#            'ftp_check_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
            'proxy_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
            'check_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
            'mail_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
            'domain_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
            'jabber_password': forms.PasswordInput(attrs={'size': 30}, render_value=True),
        }

class BaseInlineFormset(forms.models.BaseInlineFormSet):
    """
    This function validate inlines forms and
    raise ValidationError is there is a problem
    """
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:

            if form.__class__.__name__ == 'ProxyAccountForm':
                proxy_password = form.cleaned_data['proxy_password']
                check_password = form.cleaned_data['check_password']
                proxy_username = form.cleaned_data['proxy_username']
                account = form.cleaned_data['account']

                if proxy_username == '':
                    p = ProxyAccount.objects.filter(account=account)
                    for user in p:
                        if user.proxy_username.__str__() == account.__str__():
                            raise forms.ValidationError('Default Proxy account already exists.')

                if check_password != crypt.crypt(proxy_password, proxy_username):
                    if proxy_password != check_password:
                        raise forms.ValidationError('Your password must be the same')

            elif form.__class__.__name__ == 'MailAccountForm':
                mail_password = form.cleaned_data['mail_password']
                check_password = form.cleaned_data['check_password']
                mail_username = form.cleaned_data['mail_username']
                account = form.cleaned_data['account']

                if mail_username == '':
                    p = MailAccount.objects.filter(account=account)
                    for user in p:
                        if user.mail_username.__str__() == account.__str__()+ "@" + DOMAIN:
                            raise forms.ValidationError('Default Mail account already exists.')

                if check_password != crypt.crypt(mail_password, mail_username):
                    if mail_password != check_password:
                        raise forms.ValidationError('Your password must be the same')

            elif form.__class__.__name__ == 'DomainAccountForm':
                domain_password = form.cleaned_data['domain_password']
                check_password = form.cleaned_data['check_password']
                domain_username = form.cleaned_data['domain_username']
                account = form.cleaned_data['account']

                if domain_username == '':
                    p = DomainAccount.objects.filter(account=account)
                    for user in p:
                        if user.domain_username.__str__() == account.__str__():
                            raise forms.ValidationError('Default Domain account already exists.')

                if check_password != crypt.crypt(domain_password, domain_username):
                    if domain_password != check_password:
                        raise forms.ValidationError('Your password must be the same')

            elif form.__class__.__name__ == 'JabberAccountForm':
                jabber_password = form.cleaned_data['jabber_password']
                check_password = form.cleaned_data['check_password']
                jabber_username = form.cleaned_data['jabber_username']
                account = form.cleaned_data['account']

                if jabber_username == '':
                    p = JabberAccount.objects.filter(account=account)
                    for user in p:
                        if user.jabber_username.__str__() == account.__str__():
                            raise forms.ValidationError('Default Jabber account already exists.')

                if check_password != hashlib.md5(jabber_password).hexdigest():
                    if jabber_password != check_password:
                        raise forms.ValidationError('Your password must be the same')

class ProxyAccountInline(admin.StackedInline):
    model = ProxyAccount
    extra = 0
    if not DEBUG:
        form = InlineForm
    formset = BaseInlineFormset

#class FtpAccountInline(admin.StackedInline):
#    model = AccountsFtpaccount
#    extra = 0
#    if not DEBUG:
#        form = InlineForm
#    formset = BaseInlineFormset

class MailAccountInline(admin.StackedInline):
    model = MailAccount
    extra = 0
    if not DEBUG:
        form = InlineForm
    formset = BaseInlineFormset

class DomainAccountInline(admin.StackedInline):
    model = DomainAccount
    extra = 0
    if not DEBUG:
        form = InlineForm
    formset = BaseInlineFormset

class JabberAccountInline(admin.StackedInline):
    model = JabberAccount
    extra = 0
    if not DEBUG:
        form = InlineForm
    formset = BaseInlineFormset

class AccountAdmin(admin.ModelAdmin):
#    inlines = [ProxyAccountInline, MailAccountInline, JabberAccountInline, DomainAccountInline,FtpAccountInline]
    inlines = [ProxyAccountInline, MailAccountInline, JabberAccountInline, DomainAccountInline]
    list_display = ('username', 'active', 'first_name', 'last_name', 'telephone', 'department', 'created', 'modified')
    search_fields = ['username', 'personal_ID', 'first_name', 'last_name', 'entity_ID']
    ordering = ('username',)
    if not DEBUG:
        form = InlineForm

    if not DEBUG:
        fieldsets = [
            ('Status information', {'fields': ['active', 'active_begin', 'active_end']}),
            ('Personal information', {'fields': ['personal_ID', 'first_name', 'last_name', 'username', 'password', 'check_password']}),
            ('Work information',{'fields': ['entity_ID', 'telephone', 'department']}),
        ]
    # Compara los passwords si son iguales los hace crypt y al check password lo guarda como crypt del crypt
    def save_model(self, request, modelobj, form, change):
        if modelobj.password == modelobj.check_password:
            modelobj.password = crypt.crypt(modelobj.password, modelobj.username)
            modelobj.check_password = crypt.crypt(modelobj.password, modelobj.username)

        modelobj.save()

    def save_formset(self, request, form, formset, change):

        instances = formset.save(commit=False)
        for instance in instances:
            if instance.__class__.__name__ == 'ProxyAccount':
                # Obtener usuario y password de la clase padre
                p = Account.objects.get(id=instance.account_id)

                if instance.proxy_username == '':
                    instance.proxy_username = p.username

                if instance.proxy_password == '':
                    instance.proxy_password = p.password
                    instance.check_password = p.check_password
                #
                if instance.proxy_password == instance.check_password:
                    instance.proxy_password = crypt.crypt(instance.proxy_password, instance.proxy_username)
                    instance.check_password = crypt.crypt(instance.proxy_password, instance.proxy_username)

            elif instance.__class__.__name__ == 'MailAccount':
                # Obtener usuario y password de la clase padre
                p = Account.objects.get(id=instance.account_id)

                if instance.mail_username == '':
                    instance.mail_username = p.username+ "@"+ DOMAIN

                if instance.mail_password == '':
                    instance.mail_password = p.password
                    instance.check_password = p.check_password
                #
                if instance.mail_password == instance.check_password:
                    instance.mail_password = crypt.crypt(instance.mail_password, instance.mail_username)
                    instance.check_password = crypt.crypt(instance.mail_password, instance.mail_username)

                if instance.mail_location == '' or instance.mail_dir == '':
                    instance.mail_location = 'maildir:/home/vmail/%s/%s/' % (instance.mail_username.split("@")[1], instance.mail_username.split("@")[0])
                    instance.mail_dir = '%s/%s/' % (instance.mail_username.split("@")[1], instance.mail_username.split("@")[0])

            elif instance.__class__.__name__ == 'DomainAccount':
                # Obtener usuario y password de la clase padre
                p = Account.objects.get(id=instance.account_id)

                if instance.domain_username == '':
                    instance.domain_username = p.username

                if instance.domain_password == '':
                    instance.domain_password = p.password
                    instance.check_password = p.check_password
                #
                if instance.domain_password == instance.check_password:
                    self.update_pdc(instance.domain_username, instance.domain_password, 'add')
                    instance.domain_password = crypt.crypt(instance.domain_password, instance.domain_username)
                    instance.check_password = crypt.crypt(instance.domain_password, instance.domain_username)

            elif instance.__class__.__name__ == 'JabberAccount':
                # Obtener usuario y password de la clase padre
                p = Account.objects.get(id=instance.account_id)

                if instance.jabber_username == '':
                    instance.jabber_username = p.username

                if instance.jabber_password == '':
                    # instance.jabber_password = p.password
                    # instance.check_password = p.check_password
                    instance.jabber_password = hashlib.md5(p.password).hexdigest()
                    instance.check_password = instance.jabber_password
                    print p.password, instance.jabber_password

                #
                if instance.jabber_password == instance.check_password:
                    instance.jabber_password = hashlib.md5(instance.jabber_password).hexdigest()
                    instance.check_password = instance.jabber_password


            instance.save()

    # Actions
    actions = ["disable_account", "enable_account"]

    def disable_account(self, request, queryset):
        for obj in queryset:
            obj.active = 0
            obj.save()
        message = "The accounts has been disabled successfully"
        self.message_user(request, message)
    disable_account.short_description = "Disable selected accounts"

    def enable_account(self, request, queryset):
        for obj in queryset:
            obj.active = 1
            obj.save()
        message = "The accounts has been enabled successfully"
        self.message_user(request, message)
    enable_account.short_description = "Enable selected accounts"

    def update_pdc(self, obj1, obj2, command):
        message = '%s %s %s' %(command, obj1, obj2) # default text to send to server
        sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
        sockobj.connect((pdcHost, pdcPort))   # connect to server machine and port
        sockobj.send(message)                       # send line to server over socket
        sockobj.close( )                            # close socket to send eof to server

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('area', 'name',)

class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('name',)

class ProxyAccountAdmin(admin.ModelAdmin):
    list_display = ('proxy_username', 'proxy_active', 'proxy_account_type', 'created', 'modified')
    list_filter = ['proxy_account_type']
    search_fields = ['proxy_username']
    ordering = ('proxy_username',)
    if not DEBUG:
        form = InlineForm

    def save_model(self, request, modelobj, form, change):
        # Obtener usuario y password de la clase padre
        p = Account.objects.get(id=modelobj.account_id)

        if modelobj.proxy_username == '':
            modelobj.proxy_username = p.username

        if modelobj.proxy_password == '':
            modelobj.proxy_password = p.password
            modelobj.check_password = p.check_password
        #
        if modelobj.proxy_password == modelobj.check_password:
            modelobj.proxy_password = crypt.crypt(modelobj.proxy_password, modelobj.proxy_username)
            modelobj.check_password = crypt.crypt(modelobj.proxy_password, modelobj.proxy_username)

        modelobj.save()

class MailAccountAdmin(admin.ModelAdmin):
    list_display = ('mail_username', 'mail_active', 'mail_account_type', 'created', 'modified')
    list_filter = ['mail_account_type']
    search_fields = ['mail_username']
    ordering = ('mail_username',)
    if not DEBUG:
        form = InlineForm

    def save_model(self, request, modelobj, form, change):
        # Obtener usuario y password de la clase padre
        p = Account.objects.get(id=modelobj.account_id)

        if modelobj.mail_username == '':
            modelobj.mail_username = p.username+"@"+ DOMAIN

        if modelobj.mail_password == '':
            modelobj.mail_password = p.password
            modelobj.check_password = p.check_password
        #
        if modelobj.mail_password == modelobj.check_password:
            modelobj.mail_password = crypt.crypt(modelobj.mail_password, modelobj.mail_username.split("@")[0])
            modelobj.check_password = crypt.crypt(modelobj.mail_password, modelobj.mail_username.split("@")[0])

        if modelobj.mail_location == '' or modelobj.mail_dir == '':
            modelobj.mail_location = 'maildir:/home/vmail/%s/%s/' % (modelobj.mail_username.split("@")[1], modelobj.mail_username.split("@")[0])
            modelobj.mail_dir = '%s/%s/' % (modelobj.mail_username.split("@")[1], modelobj.mail_username.split("@")[0])

        modelobj.save()

class MailAliasAdmin(admin.ModelAdmin):
    list_display = ('mail_alias', 'mail_goto', 'created', 'modified')
    list_filter = ['mail_account_type']
    search_fields = ['mail_alias']
    ordering = ('mail_alias',)

class DomainAccountAdmin(admin.ModelAdmin):
    list_display = ('domain_username', 'domain_active', 'domain_group', 'created', 'modified')
    list_filter = ['domain_group']
    search_fields = ['domain_username']
    ordering = ('domain_username',)
    if not DEBUG:
        form = InlineForm

    def save_model(self, request, modelobj, form, change):
        # Obtener usuario y password de la clase padre
        p = Account.objects.get(id=modelobj.account_id)

        if modelobj.domain_username == '':
            modelobj.domain_username = p.username

        if modelobj.domain_password == '':
            modelobj.domain_password = p.password
            modelobj.check_password = p.check_password
        #
        if modelobj.domain_password == modelobj.check_password:
            self.update_pdc(modelobj.domain_username, modelobj.domain_password, 'add')
            modelobj.domain_password = crypt.crypt(modelobj.domain_password, modelobj.domain_username)
            modelobj.check_password = crypt.crypt(modelobj.domain_password, modelobj.domain_username)

        modelobj.save()

    def update_pdc(self, obj1, obj2, command):
        message = '%s %s %s' %(command, obj1, obj2)  # default text to send to server
        sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
        sockobj.connect((pdcHost, pdcPort))   # connect to server machine and port
        sockobj.send(message)                       # send line to server over socket
        sockobj.close( )                            # close socket to send eof to server

    # Actions
    actions = ["delete_account"]

    def delete_account(self, request, queryset):
        for obj in queryset:
            self.update_pdc(obj.domain_username, obj.domain_password, 'del')
            obj.delete()
        message = "The accounts has been deleted successfully"
        self.message_user(request, message)
    delete_account.short_description = "Full delete selected accounts"

class JabberAccountAdmin(admin.ModelAdmin):
    list_display = ('jabber_username', 'jabber_active', 'created', 'modified')
    #list_filter = ['domain_group']
    search_fields = ['jabber_username']
    ordering = ('jabber_username',)
    if not DEBUG:
        form = InlineForm

    def save_model(self, request, modelobj, form, change):
        # Obtener usuario y password de la clase padre
        p = Account.objects.get(id=modelobj.account_id)

        if modelobj.jabber_username == '':
            modelobj.jabber_username = p.username

            if modelobj.jabber_password == '':
            # modelobj.jabber_password = p.password
            # modelobj.check_password = p.check_password
                modelobj.jabber_password =hashlib.md5(p.password).hexdigest()
                modelobj.check_password = hashlib.md5(p.password).hexdigest()

        #
        if modelobj.jabber_password == modelobj.check_password:
            modelobj.jabber_password = hashlib.md5(modelobj.jabber_password).hexdigest()
            modelobj.check_password = modelobj.jabber_password
	    #hashlib.md5(modelobj.jabber_password).hexdigest()

        modelobj.save()

#class AccountsFtpaccountAdmin(admin.ModelAdmin):
#    list_display = ('ftp_username', 'ftp_path')
    #list_filter = ['domain_group']
#    search_fields = ['ftp_username']
#    ordering = ('ftp_username',)
#    if not DEBUG:
#       form = InlineForm



class ProxyQuotaTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('name',)

class ProxyAccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('name',)

class MailAccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('name',)

class DomainGroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ['name']
    ordering = ('name',)

# Register sites.
admin.site.register(Account, AccountAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(ProxyAccount, ProxyAccountAdmin)
admin.site.register(MailAccount, MailAccountAdmin)
admin.site.register(MailAlias, MailAliasAdmin)
admin.site.register(DomainAccount, DomainAccountAdmin)
admin.site.register(JabberAccount, JabberAccountAdmin)
#admin.site.register(AccountsFtpaccount,AccountsFtpaccountAdmin)

if ALL_VIEWS:
    admin.site.register(ProxyQuotaType, ProxyQuotaTypeAdmin)
    admin.site.register(ProxyAccountType, ProxyAccountTypeAdmin)
    admin.site.register(MailAccountType, MailAccountTypeAdmin)
    admin.site.register(DomainGroupType, DomainGroupTypeAdmin)
