
from django.conf.urls import url

from company import views as company_views


urlpatterns = [

    # HTML views
    url(
        r"^$",
        company_views.account,
        name="account"
    ),
    url(
        r"^subscribe/$",
        company_views.subscribe,
        name="subscribe"
    ),
    url(
        r"^confirm/(?P<plan>.+)$",
        company_views.confirm,
        name="confirm"
    ),
    url(
        r"^change/plan/$",
        company_views.change_plan,
        name="change_plan"
    ),
    url(
        r"^change/cards/$",
        company_views.change_card,
        name="change_card"
    ),
    # NOTE: cancellation not allowed (free plan available)
    # url(
    #     r"^cancel/subscription/$",
    #     'company.views.cancel_subscription',
    #     name="cancel_subscription"
    # ),
    url(
        r"^history/$",
        company_views.history,
        name="history"
    ),
    url(
        r"^invoice/(?P<pk>\d+)/$",
        company_views.invoice,
        name="invoice"
    ),


    # Web services
    url(
        r"^a/sync/history/$",
        company_views.sync_history,
        name="sync_history"
    ),
]
