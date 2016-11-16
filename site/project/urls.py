from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.i18n import javascript_catalog
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.sitemaps import FlatPageSitemap

from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap

from rest_framework import routers
from rest_framework.authtoken import views

from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from services.rest.views import (
    ShareholderViewSet, CompanyViewSet, UserViewSet,
    PositionViewSet,
    InviteeUpdateView, AddCompanyView, CountryViewSet, OptionPlanViewSet,
    SecurityViewSet, OptionTransactionViewSet, OperatorViewSet, AddShareSplit,
    LanguageView, AvailableOptionSegmentsView
)

from shareholder.views import ShareholderView

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

js_info_dict = {
    'packages': ('project', 'shareholder', 'utils', 'services',),
}

sitemaps = {'tags': TagSitemap,
            'blog': EntrySitemap,
            'authors': AuthorSitemap,
            'categories': CategorySitemap,
            'pages': FlatPageSitemap,
            }

urlpatterns = [
    # web views
    url(r'^$', 'project.views.index', name='index'),  # landing page
    url(r'^start/$', 'project.views.start', name='start'),  # user home
    url(r'^positions/$', 'shareholder.views.positions', name='positions'),
    url(r'^shareholder/(?P<pk>[0-9]+)/$',
        ShareholderView.as_view(), name='shareholder'),

    url(r'^company/(?P<company_id>[0-9]+)/$', 'company.views.company',
        name='company'),
    url(r'^company/(?P<company_id>[0-9]+)/download/csv$',
        'project.views.captable_csv', name='captable_csv'),
    url(r'^company/(?P<company_id>[0-9]+)/download/pdf$',
        'project.views.captable_pdf', name='captable_pdf'),
    url(r'^options/$', 'shareholder.views.options', name='options'),
    url(r'^optionsplan/(?P<optionsplan_id>[0-9]+)/$',
        'shareholder.views.optionsplan', name='optionplan'),
    url(r'^optionsplan/(?P<optionsplan_id>[0-9]+)/download/pdf/$',
        'shareholder.views.optionsplan_download_pdf',
        name='optionplan_download_pdf'),
    url(r'^optionsplan/(?P<optionsplan_id>[0-9]+)/download/img/$',
        'shareholder.views.optionsplan_download_img',
        name='optionplan_download_img'),

    # auth
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^instapage/', 'project.views.instapage', name='instapage'),

    # rest api
    url(r'^services/rest/company/add', AddCompanyView.as_view(),
        name='add_company'),
    url(r'^services/rest/split', AddShareSplit.as_view(), name='split_shares'),
    url(r'^services/rest/optionplan/(?P<optionsplan_id>[0-9]+)/number_segments/'
        r'(?P<shareholder_id>[0-9]+)', AvailableOptionSegmentsView.as_view(),
        name='available_option_segments'),  # before router!
    url(r'^services/rest/', include(router.urls)),
    url(r'^services/rest/invitee', InviteeUpdateView.as_view(),
        name='invitee'),
    url(r'^services/rest/language', LanguageView.as_view(),
        name='language'),
    # url(r'^api-auth/', include('rest_framework.urls',
    #    namespace='rest_framework')),
    url(r'^services/rest/api-token-auth/',
        views.obtain_auth_token),  # allow to see token for the logged in user

    # i18n
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),

    # content/blog/flatpages
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
]

# admin
admin.autodiscover()
admin_url = settings.DEBUG and r'^admin/' or r'^__adm/'
urlpatterns += patterns(
    '',
    url(admin_url, include(admin.site.urls)),
)

# rosetta
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# serving files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^_403/$', TemplateView.as_view(template_name="403.html")),
        (r'^_404/$', TemplateView.as_view(template_name="404.html")),
        (r'^_500/$', TemplateView.as_view(template_name="500.html")),
    )

# sitemap
urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'index',
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap',
        {'sitemaps': sitemaps}),)

# flatpages (MUST be end of pattern) + markdown
urlpatterns += [
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^(?P<url>.*/)$', flatpage),
]
