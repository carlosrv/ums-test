from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.

##################################
SERVICE_VALID_DAYS = 366
PROXY_CUOTA_DEFAULT = 100
MAIL_CUOTA_DEFAULT = 100
##################################

from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import crypt
from django.utils import timezone
#import win_crypt as crypt

class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    area = models.ForeignKey(Area)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    active = models.BooleanField()                     # TODO: status
    active_begin = models.DateField(default=timezone.now)
    active_end = models.DateField(default=datetime.now()+timedelta(days=SERVICE_VALID_DAYS))
    #photo = models.ImageField(blank=True, upload_to='photos')
    personal_ID = models.CharField(max_length=11)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    check_password = models.CharField(max_length=100)
    entity_ID = models.CharField(blank=True, max_length=100)
    telephone = models.CharField(blank=True, max_length=100)    # TODO: models.PhoneNumberField()
    department = models.ForeignKey(Department)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def clean(self):
        if self.check_password != crypt.crypt(self.password, self.username):
            if self.password != self.check_password:
                raise ValidationError("Your password must be the same")

class ProxyQuotaType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProxyAccountType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProxyAccount(models.Model):
    proxy_active = models.BooleanField()
    proxy_active_begin = models.DateField(default=timezone.now)
    proxy_active_end = models.DateField(default=datetime.now()+timedelta(days=SERVICE_VALID_DAYS))
    proxy_username = models.CharField(max_length=100, unique=True, blank=True)
    proxy_password = models.CharField(max_length=100, blank=True)
    check_password = models.CharField(max_length=100, blank=True)
    proxy_quota = models.PositiveIntegerField(default= PROXY_CUOTA_DEFAULT)
    proxy_quota_extra = models.PositiveIntegerField(default=0)
    proxy_quota_type = models.ForeignKey(ProxyQuotaType)
    proxy_account_type = models.ForeignKey(ProxyAccountType)
    account = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.proxy_username

    def clean(self):
        if self.check_password != crypt.crypt(self.proxy_password, self.proxy_username):
            if self.proxy_password != self.check_password:
                raise ValidationError("Your password must be the same")

class MailAccountType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MailAccount(models.Model):
    mail_active = models.BooleanField()
#    webmail_external_access = models.BooleanField()
    mail_active_begin = models.DateField(default=timezone.now)
    mail_active_end = models.DateField(default=datetime.now()+timedelta(days=SERVICE_VALID_DAYS))
    mail_username = models.EmailField(max_length=100, unique=True, blank=True)
    mail_password = models.CharField(max_length=100, blank=True)
    check_password = models.CharField(max_length=100, blank=True)
    mail_quota = models.PositiveIntegerField(default= MAIL_CUOTA_DEFAULT)
    mail_account_type = models.ForeignKey(MailAccountType)
    mail_location = models.CharField(max_length=100, blank=True)
    mail_dir = models.CharField(max_length=100, blank=True)
    account = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mail_username

    def clean(self):
        if self.check_password != crypt.crypt(self.mail_password, self.mail_username):
            if self.mail_password != self.check_password:
                raise ValidationError("Your password must be the same")

class MailAlias(models.Model):
    mail_alias = models.EmailField(max_length=100)
    mail_goto = models.EmailField(max_length=100)
    mail_account_type = models.ForeignKey(MailAccountType)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mail_alias

class DomainGroupType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DomainAccount(models.Model):
    domain_active = models.BooleanField()
    domain_active_begin = models.DateField(default=timezone.now)
    domain_active_end = models.DateField(default=datetime.now()+timedelta(days=SERVICE_VALID_DAYS))
    domain_username = models.CharField(max_length=100, unique=True, blank=True)
    domain_password = models.CharField(max_length=100)
    check_password = models.CharField(max_length=100)
    domain_group = models.ForeignKey(DomainGroupType)
    account = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.domain_username

    def clean(self):
        if self.check_password != crypt.crypt(self.domain_password, self.domain_username):
            if self.domain_password != self.check_password:
                raise ValidationError("Your password must be the same")

class JabberAccount(models.Model):
    jabber_active = models.BooleanField()
    jabber_active_begin = models.DateField(default=timezone.now)
    jabber_active_end = models.DateField(default=datetime.now()+timedelta(days=SERVICE_VALID_DAYS))
    jabber_username = models.CharField(max_length=100, unique=True, blank=True)
    jabber_password = models.CharField(max_length=100, blank=True)
    check_password = models.CharField(max_length=100, blank=True)
    account = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.jabber_username

    def clean(self):
        if self.check_password != crypt.crypt(self.jabber_password, self.jabber_username):
            if self.jabber_password != self.check_password:
                raise ValidationError("Your password must be the same")


class AccountsFtpaccount(models.Model):
    ftp_username = models.CharField(max_length=100L, unique=True)
    ftp_password = models.CharField(max_length=100L)
    ftp_check_password = models.CharField(max_length=100L)
    ftp_path = models.CharField(max_length=100L)
    account_id = models.ForeignKey(Account)

    def __unicode__(self):
        return self.ftp_username

    def clean(self):
        if self.ftp_check_password != crypt.crypt(self.ftp_password, self.ftp_username):
            if self.ftp_password != self.ftp_check_password:
                raise ValidationError("Your password must be the same")


    class Meta:
        db_table = 'accounts_ftpaccount'


