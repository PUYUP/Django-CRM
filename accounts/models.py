from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import User, Address, Team
from common.utils import INDCHOICES
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify


class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique = True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)



class Account(models.Model):

    ACCOUNT_STATUS_CHOICE = (
        ("open", "Open"),
        ('close', 'Close')
    )

    name = models.CharField(pgettext_lazy("Name of Account", "Name"), max_length=64)
    email = models.EmailField()
    phone = PhoneNumberField(null=True)
    industry = models.CharField(_("Industry Type"), max_length=255, choices=INDCHOICES, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='account_billing_address', on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.ForeignKey(Address, related_name='account_shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(User, related_name='account_assigned_to')
    teams = models.ManyToManyField(Team)
    created_by = models.ForeignKey(User, related_name='account_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICE, max_length=64, default='open')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']
