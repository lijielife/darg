.. role:: python(code)
   :language: python

Subscriptions
=============

Companies require an active subscription to access most features of
das-aktienregister.ch. Accessable without subscriptions are pure company
related information like company detail data or operators.

Subscriptions are handled via https://stripe.com and an account is required
to access the app (even for testing).

Settings
--------

:python:`STRIPE_PUBLIC_KEY`
:python:`get_env_variable('STRIPE_PUBLIC_KEY')`

   public strip key

   **NOTE:** set this to `'test' not in sys.argv and '<KEY>' or ''`

:python:`STRIPE_SECRET_KEY`
:pyhton:`get_env_variable('STRIPE_SECRET_KEY')`

   secret stripe key

   **NOTE:** set this to `'test' not in sys.argv and '<KEY>' or ''`

:python:`DJSTRIPE_INVOICE_FROM_EMAIL`
:python:`DEFAULT_FROM_EMAIL`

   email sender address of invoices

:python:`DJSTRIPE_SUBSCRIBER_MODEL`
:python:`'shareholder.Company'`

   typically a user, but we use subscriptions for company objects

:python:`DJSTRIPE_CURRENCIES`
:python:`(('chf', _('Swiss franc'),),)`

   currencies available on checkout

:python:`DJSTRIPE_PLANS`

   see STRIPE_PLANS_

:python:`DJSTRIPE_SUBSCRIBER_MODEL_REQUEST_CALLBACK`
:python:`utils.subscriptions.stripe_subscriber_request_callback`

   callback to get subscriber (company) from request

:python:`SUBSCRIPTION_FEATURES`

   see SUBSCRIPTION_FEATURES_

:python:`DEFAULT_HTTP_PROTOCOL`
:python:`'https'`

   used by djstripe when sending emails

:python:`COMPANY_INVOICES_ROOT`
:python:`os.path.join(SENDFILE_ROOT, 'company', 'invoices')`

   filedir-root of invoices

:python:`COMPANY_INVOICE_FILENAME`
:python:`u'das-aktienregister-rechnung'`

   filename of invoices

   **NOTE:** invoice id will be added to invoice filename

:python:`COMPANY_INVOICE_INCLUDE_VAT`
:python:`True`

   whether to include VAT in company (pdf) invoices or not

:python:`COMPANY_INVOICE_VAT`
:python:`19`

   VAT in percent

:python:`COMPANY_INVOICE_INCLUDE_IN_EMAIL`
:python:`None` (unset)

   set this to True to include all invoice items directly into the invoice
   email. If not set, the items will only we included, if pdf invoice is
   missing. If this is set to False, items will never be included in email

:python:`INVOICE_FROM_ADDRESS`
:python:`[
    'KKD Komm. GmbH',
    'Pulsnitzer Str. 52',
    '01936 Grossnaundorf',
    'Deutschland'
]`

   address of invoice (lines)


STRIPE_PLANS
------------

Subscription plans are configured in settings.
Currently there are 3 configured plans.

There a 2 customized keys for plans:

 - features: all available features for a plan (and configuration)
 - validators: validators that must be passed to be able to subscribe to this
   plan

.. code-block :: python

   DJSTRIPE_PLANS = collections.OrderedDict((
       ('startup', {
           'stripe_plan_id': 'startup',
           'name': _('StartUp'),
           'description': _(u'Designed für StartUps und Neugründungen'),
           'price': 0,
           'currency': 'chf',
           'interval': 'month',
           'features': {
               'shareholders': {
                   'max': 20,
                   'validators': {
                       'create': [
                           'company.validators.features.ShareholderCreateMaxCountValidator'
                       ]
                   }
               },
               'positions': {},
               'options': {},
               'securities': {
                   'max': 1,
                   'validators': {
                       'create': [
                           'company.validators.features.SecurityCreateMaxCountValidator'
                       ]
                   }
               },
               'shares': {},
               'gafi': {},
               'revision': {}
           },
           'validators': [
               'company.validators.features.ShareholderCountPlanValidator',
               'company.validators.features.SecurityCountPlanValidator'
           ]
       }),
       ('professional', {
           'stripe_plan_id': 'professional',
           'name': _('Professional'),
           'description': _(u'Für etablierte Aktiengesellschaften und KMU'),
           'price': 1799,  # 17.99
           'currency': 'chf',
           'interval': 'month',
           'features': {
               'shareholders': {
                   'price': 49,  # 0.49
                   'validators': {
                       'create': []
                   }
               },
               'positions': {},
               'options': {},
               'securities': {
                   'price': 1500,  # 15.00 CHF per month
                   'validators': {
                       'create': []
                   }
               },
               'shares': {},
               'gafi': {},
               'revision': {},
               'shareholder_statements': {},
               'numbered_shares': {},
               'email_support': {}
           },
           'validators': []
       }),
       ('enterprise', {
           'stripe_plan_id': 'enterprise',
           'name': _('Enterprise'),
           'description': _(
               u'First-Class-Service für grosse Aktionärsgesellschaften'),
           'price': 17900,  # 179.00
           'currency': 'chf',
           'interval': 'month',
           'features': {
               'shareholdes': {
                   'price': 9,  # 0.09
                   'validators': {
                       'create': []
                   }
               },
               'positions': {},
               'options': {},
               'securities': {
                   'price': 1500,  # 15.00 CHF per month
                   'validators': {
                       'create': []
                   }
               },
               'shares': {},
               'gafi': {},
               'revision': {},
               'shareholder_statements': {},
               'numbered_shares': {},
               'email_support': {},
               'shareholder_admin_pro': {},
               'premium_support': {},
               'custom_export_import': {}
           },
           'validators': []
       })
   ))


SUBSCRIPTION_FEATURES
---------------------

All features available. Planspecific features are configured in STRIPE_PLANS_

.. code-block :: python

   SUBSCRIPTION_FEATURES = collections.OrderedDict((
       ('shareholders', {'title': _('Shareholders'), 'core': True}),
       ('positions', {'title': _('Positions'), 'core': True}),
       ('options', {'title': _('Options'), 'core': True}),
       ('securities', {'title': _('Securities'), 'core': True}),
       ('shares', {
           'title': _(u'Aktienausgabe, Aktienkauf, -verkauf, '
                      u'Kapitalerhöhung, Aktiensplit')
       }),
       ('gafi', {'title': _('GAFI Validierung')}),
       ('revision', {'title': _('Revisionssicherheit')}),
       ('shareholder_statements', {
           'title': _('Depotauszug Email & Brief'),
           'annotation': _('Es entstehen weitere Kosten bei Briefversand '
                           'pro versendetem Brief.'),
           'form_fields': [
               'is_statement_sending_enabled',
               'statement_sending_date'
           ]
       }),
       ('numbered_shares', {'title': _('Nummerierte Aktien')}),
       ('email_support', {'title': _('Email Support')}),
       ('shareholder_admin_pro', {'title': _(u'Profi-Verwaltung Aktionäre')}),
       ('premium_support', {'title': _('Premium-Support 24/7')}),
       ('custom_export_import', {'title': _('Custom Export/Import')})
   ))

Middleware
----------

``company.middleware.CompanySubscriptionRequired``

   middleware to make sure a company has an active subscription

Middleware will check if any blacklisted (subscription required) url is
requested and will redirect, if no active subscription for company is found.

::

   BLACKLIST_URLS = [
        r'^positions/',
        r'^options/',
        r'^shareholder/',
        r'^optionsplan/'
    ]


Mixins
------

``company.mixins.CompanyOperatorPermissionRequiredViewMixin``

   view mixin to check if user is operator for company

   ``dispatch(self, request, *args, **kwargs)``

``company.mixins.SubscriptionMixin``

   mixin to check for subscription and plan features

   ``check_subscription(self, subscriber, features=None)``

      return boolean if subscriber has valid subscription
      also check for specific feature if given (str or list)

``company.mixins.SubscriptionViewMixin``

   mixin to handle subscription for view(set)s

   inherits from SubscriptionMixin

   ``COMPANY_QUERY_VAR``

      query parameter for company (default: ``company``)

   ``subscription_features``

      list of subscription features required (default: ``[]``)

   ``get_user_companies(self)``

      must be implemented in view (will raise NotImplementedError otherwise)

   ``get_company_pks()``

      return a list of company ids that have subscription (to use feature)

Subscribing
-----------

A company operator can view or change the current subscription for a company.

URL scheme is: /company/<PK>/subscriptions/

The following urls are enabled:

   - / - account overview
   - subscribe/ - subscription overview (shows all plans)
   - confirm/<plan>/ - subscribe to a plan (also checkout if required)
   - change/plan/ - change subscription
   - change/cards/ - change credit card
   - history/ - history view (includes link to PDF invoice)
   - invoice/<PK>/ - download PDF invoice
   - a/sync/history/ - stripe synchronization webservice

If the company does not have a email set, the email will be requested on stripe
checkout.

If the company does not have an address set, the address will be requested on
stripe checkout.

On first subscription, all invoice items (plan price, price pre shareholder,
price per secrurity) will be added immediately to the invoice because it will
be closed instantly. If an subscription period passes and a new invoice is
generated, Webhooks_ will be called and additional invoice items will be added
via event handlers.

**NOTE:** Cancellation of subscriptions is disabled (for now)!


Invoices
--------

PDF invoices are generated for all invoices from stripe, even if they do not
have charged the customer, to keep invoice numbers steady.

Invoice generation can be triggered on several points (admin/management
command, on-demand PDF view) but the Webhook_ signal handler for
invoice.payment_succeeded will (re)generate the PDF file.

If there is a charge, the customer (company.email) will receive an email with
the invoice (optionally with invoice items inlined, see Settings_) and attached
PDF file.


Webhooks
--------

Configure webhooks in stripe with the following URL

   /_stripe/webhooks/

Though we do not handle all events, we should keep track of what is going on
and fetch all events (will be stored in database)

``company.event_handlers.invoice_created_webhook_handler``

   *webhook signal*: invoice.created

   handler for invoice.created event

   add any pending invoice items if invoice not closed yet

   calls ``utils.subscriptions.stripe_company_shareholder_invoice_item`` and
   ``utils.subscriptions.stripe_company_security_invoice_item``


``company.event_handlers.invoice_payment_succeeded_webhook_handler``

   *webhook signal*: invoice.payment_succeeded

   handler for invoice.payment_succeeded event

   trigger invoice pdf (re)generation

``company.event_handlers.customer_webhook_handler``

   *webhook signals*: customer

   use customer email address for subscriber if no email set on subscriber
   instance, also set address (if necessary/possible)
