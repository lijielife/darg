from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.flatpages.views import flatpage
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from djstripe.views import WebHook
from django.views.decorators.cache import cache_page
from django.views.i18n import javascript_catalog  # JavaScriptCatalog
from django.contrib.sitemaps import views as sitemap_views
from registration.backends.simple.views import RegistrationView
from rest_framework import routers
from rest_framework.authtoken import views
from two_factor.admin import AdminSiteOTPRequired
from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
from two_factor.urls import urlpatterns as tf_urls
from zinnia.sitemaps import (AuthorSitemap, CategorySitemap, EntrySitemap,
                             TagSitemap)

from company import views as company_views
from project import views as project_views
from project.forms import RegistrationForm
from services.rest.views import (AddCompanyView, AddShareSplit,
                                 AvailableOptionSegmentsView, BankView,
                                 CompanyViewSet, CountryViewSet,
                                 InviteeUpdateView, LanguageView,
                                 OperatorViewSet, OptionPlanViewSet,
                                 OptionTransactionViewSet, PositionViewSet,
                                 ReportViewSet, SecurityViewSet,
                                 ShareholderViewSet, UserViewSet)
from shareholder.views import (OptionTransactionView, PositionView,
                               ShareholderView, OptionTransactionsView, OptionPlanView,
                               optionsplan_download_img,
                               optionsplan_download_pdf, PositionsView)
from shareholder import views as shareholder_views

# API routes
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'shareholders', ShareholderViewSet, base_name="shareholders")
router.register(r'operators', OperatorViewSet, base_name="operators")
router.register(r'company', CompanyViewSet)
router.register(r'user', UserViewSet, base_name="user")
router.register(r'position', PositionViewSet, base_name="position")
router.register(r'country', CountryViewSet, base_name="country")
router.register(r'optionplan', OptionPlanViewSet, base_name="optionplan")
router.register(r'optiontransaction', OptionTransactionViewSet,
                base_name="optiontransaction")
router.register(r'security', SecurityViewSet, base_name="security")
router.register(r'report', ReportViewSet, base_name="report")


# SITEMAP conf
sitemaps = {'tags': TagSitemap,
            'blog': EntrySitemap,
            'authors': AuthorSitemap,
            'categories': CategorySitemap,
            'pages': FlatPageSitemap,
            }

# main url conf
urlpatterns = [
    # web views
    url(r'^$', project_views.index, name='index'),  # landing page
    url(r'^start/$', project_views.start, name='start'),  # user home

    url(r'^positions/$', PositionsView.as_view(), name='positions'),
    url(r'^positions/(?P<pk>[0-9]+)/$',
        PositionView.as_view(), name='position'),
    url(r'^positions/(?P<option_id>[0-9]+)/download/pdf$',
        shareholder_views.position_option_pdf, name='position_option_pdf'),

    url(r'^shareholder/(?P<pk>[0-9]+)/$',
        ShareholderView.as_view(), name='shareholder'),

    url(r'^company/$', company_views.company_select,
        name='company_list'),
    url(r'^company/(?P<company_id>[0-9]+)/$', company_views.company,
        name='company'),

    url(r'^options/$', OptionTransactionsView.as_view(), name='options'),
    url(r'^options/(?P<pk>[0-9]+)/$',
        OptionTransactionView.as_view(), name='optiontransaction'),
    url(r'^options/(?P<option_id>[0-9]+)/download/pdf$',
        shareholder_views.option_pdf, name='option_pdf'),

    url(r'^optionsplan/(?P<pk>[0-9]+)/$',
        OptionPlanView.as_view(), name='optionplan'),
    url(r'^optionsplan/(?P<optionsplan_id>[0-9]+)/download/pdf/$',
        optionsplan_download_pdf,
        name='optionplan_download_pdf'),
    url(r'^optionsplan/(?P<optionsplan_id>[0-9]+)/download/img/$',
        optionsplan_download_img,
        name='optionplan_download_img'),

    # reports
    url(r'^reports/', include('reports.urls', namespace='reports')),

    # --- auth
    # disable dj registration login
    url(r'^accounts/login/$', RedirectView.as_view(url='/account/login/'),
        name='auth_login'),
    url(r'^accounts/register/$', RegistrationView.as_view(
         form_class=RegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include(tf_urls + tf_twilio_urls, 'two_factor')),  # two factorauth
    url(r'^instapage/', project_views.instapage, name='instapage'),

    # rest api
    url(r'^services/rest/company/add', AddCompanyView.as_view(),
        name='add_company'),
    url(r'^services/rest/split', AddShareSplit.as_view(), name='split_shares'),
    url(r'^services/rest/optionplan/(?P<optionsplan_id>[0-9]+)/number_segments/'
        r'(?P<shareholder_id>[0-9]+)', AvailableOptionSegmentsView.as_view(),
        name='available_option_segments'),  # before router!
    url(r'^services/rest/', include(router.urls)),
    url(r'^services/rest/bank', BankView.as_view(),
        name='banks'),
    url(r'^services/rest/invitee', InviteeUpdateView.as_view(),
        name='invitee'),
    url(r'^services/rest/language', LanguageView.as_view(),
        name='language'),
    # url(r'^api-auth/', include('rest_framework.urls',
    #    namespace='rest_framework')),
    url(r'^services/rest/api-token-auth/',
        views.obtain_auth_token),  # allow to see token for the logged in user

    # i18n
    # url(r'^jsi18n/$', javascript_catalog JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript-catalog'),

    # content/blog
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^markdown/', include('django_markdown.urls')),

    # shareholder/user statements
    url(r'^statements/$',
        shareholder_views.statement_list,
        name='statements'),
    url(r'^statements/download/pdf/$',
        shareholder_views.statement_download_pdf,
        name='statement_download_pdf'),
    url(r'^allstatements/download/pdf/$',
        shareholder_views.all_statements_download_pdf,
        name='all_statements_download_pdf'),
    url(r'^statements/reports/$',
        shareholder_views.statement_report_list,
        name='statement_reports'),
    url(r'^statements/reports/(?P<pk>\d+)/$',
        cache_page(60*60*24)(shareholder_views.statement_report_detail),
        name='statement_report'),

    # stripe
    url(r'^subscriptions/$', company_views.subscriptions,
        name='subscriptions'),
    url(r'^company/(?P<company_id>[0-9]+)/subscriptions/',
        include('company.urls_djstripe', namespace="djstripe")),
    url(r'^_stripe/webhooks/$', WebHook.as_view()),

    # chrome needs this:
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/compiled/images/favicon.ico')),
]

# admin
if not settings.DEBUG:
    admin.site.__class__ = AdminSiteOTPRequired
admin.autodiscover()
admin_url = settings.DEBUG and r'^admin/' or r'^__adm/'
urlpatterns += [url(admin_url, include(admin.site.urls))]


# rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls'))]

# serving files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^_403/$', TemplateView.as_view(template_name="403.html")),
    url(r'^_404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^_500/$', TemplateView.as_view(template_name="500.html")),
]

# sitemap
urlpatterns += [
    url(r'^sitemap.xml$', sitemap_views.index,
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap,
        {'sitemaps': sitemaps})
    ]

# flatpages (MUST be end of pattern) + markdown
urlpatterns += [
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^(?P<url>.*/)$', flatpage, name='flatpage'),
]
