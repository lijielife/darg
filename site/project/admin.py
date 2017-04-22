#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from djstripe.admin import (Customer, CurrentSubscription, subscription_status,
                            CustomerHasCardListFilter,
                            CustomerSubscriptionStatusListFilter)
from markdownx.widgets import AdminMarkdownxWidget
# from reversion.admin import VersionAdmin  # revers > 2.0
from flatpage_meta.admin import ReplacementFlatPageAdmin

from reversion.admin import VersionAdmin  # revers > 2.0


UserAdmin.list_display = (
    'email',
    'first_name',
    'last_name',
    'is_active',
    'last_login',
    'date_joined',
    'is_staff')
UserAdmin.list_filter = (
    'is_staff', 'date_joined', 'operator__company', 'shareholder__company',
    'last_login',
    )


class ReversionedUserAdmin(VersionAdmin, UserAdmin):

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'last_login',
        'date_joined',
        'is_staff')

    list_filter = (
        'is_staff', 'date_joined', 'operator__company', 'shareholder__company',
        'last_login',
        )


class FlatPageAdminX(ReplacementFlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class CurrentSubscriptionInline(admin.StackedInline):
    model = CurrentSubscription


class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = ('subscriber',)
    readonly_fields = ('created',)
    list_display = ("stripe_id", "subscriber", "card_kind", "card_last_4",
                    subscription_status, "created")
    list_filter = ("card_kind", CustomerHasCardListFilter,
                   CustomerSubscriptionStatusListFilter)
    search_fields = ("stripe_id",)
    fieldsets = (
        (None, dict(fields=('stripe_id', 'subscriber', 'created'))),
        (_('Card'), dict(fields=('card_fingerprint', 'card_last_4',
                                 'card_kind',
                                 ('card_exp_month', 'card_exp_year'))))
    )
    inlines = (CurrentSubscriptionInline,)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminX)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Customer)
admin.site.register(Customer, CustomerAdmin)
