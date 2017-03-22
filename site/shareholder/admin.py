from django.contrib import admin
from reversion.admin import VersionAdmin

from shareholder.models import (Bank, Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder, UserProfile)


class ShareholderAdmin(VersionAdmin):
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    list_filter = ('company',)


class CompanyAdmin(VersionAdmin):
    pass


class BankAdmin(VersionAdmin):
    pass


class OperatorAdmin(VersionAdmin):
    list_display = ('id', 'user', 'company', 'date_joined')
    list_filter = ('company',)

    def date_joined(selfi, obj):
        return obj.user.date_joined


class PositionAdmin(VersionAdmin):
    list_display = (
        'bought_at', 'get_buyer', 'get_seller', 'count', 'value', 'get_company'
        )
    list_filter = ('buyer__company', 'seller__company')
    search_fields = [
        'buyer__user__email', 'seller__user__email',
        'buyer__company__name', 'seller__company__name'
    ]

    def get_seller(self, obj):
        if obj.seller:
            return obj.seller.user.email
        return None

    def get_buyer(self, obj):
        if obj.buyer:
            return obj.buyer.user.email
        return None

    def get_company(self, obj):
        if obj.buyer:
            return obj.buyer.company
        elif obj.seller:
            return obj.seller.company
        return None


class UserProfileAdmin(VersionAdmin):
    list_display = ('user', 'full_name', 'street',
                    'street2', 'city')
    search_fields = [
        'user__first_name', 'user__email', 'user__last_name', 'user__username',
    ]

    def full_name(self, obj):
        return u'{} {}'.format(obj.user.first_name, obj.user.last_name)


class CountryAdmin(VersionAdmin):
    list_display = ('iso_code',)
    search_fields = ['iso_code', 'name']


class SecurityAdmin(VersionAdmin):
    list_display = ('title', 'company', 'face_value')
    list_filter = ('company',)


class OptionTransactionAdmin(VersionAdmin):
    list_display = ('bought_at', 'buyer', 'seller',)
    pass


class OptionPlanAdmin(VersionAdmin):
    list_display = ('title',)
    list_filter = ('company',)


admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(OptionPlan, OptionPlanAdmin)
admin.site.register(OptionTransaction, OptionTransactionAdmin)
admin.site.register(Bank, BankAdmin)
