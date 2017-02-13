Aktienregister Restful API
=============================================

We are using the `Django Rest Framework <http://www.django-rest-framework.org/>`_ for the API. Please read there for more details.

General
----------------

All api endpoints are residing under ``/services/rest/`` and require token based authentication.

Authentication
----------------

We are using `Token based authentication <http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication>`_. As recommended we are creating a new token for each new user by default.

Please note that for authentication the header must be sent with any request. e.g.:

    Authorization: Token 9944b09199c62bc22418ad846dd0e4bbdfc6ee4b

Authentication can be tested and validated as follows:

.. code-block :: shell

    curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

To obtain the toke a dedicated view view will return a JSON response when valid username and password fields are POSTed to the view using form data or JSON:

.. code-block :: json

    { "token" : "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }

The view is under ``services/rest/api-token-auth/`` and requires a ``POST`` with username and password attributes.


Permissions
-----------

Most of the api endpoints require an operator permission
(user must be authenticated and operator of at least one company).

Some enpoints also require an active company subscription

    - shareholders
    - share splits
    - positions
    - securities
    - optionplans
    - optiontransactions


Shareholder list and details
-----------------------------------------------------------------------------

Resource Name: ``shareholders``

To obtain the shareholder data for the authenticated user a simple GET call to this endpoint.

    GET /services/rest/shareholders

will return this payload

.. code-block :: json

    HTTP 200 OK
    Content-Type: application/json
    Vary: Accept
    Allow: GET, POST, HEAD, OPTIONS

    {
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "pk": 51,
                "user": {
                    "first_name": "Mertesacker",
                    "last_name": "Peer",
                    "email": "peer@someemail.de",
                    "operator_set": []
                },
                "number": "56789",
                "company": {
                    "pk": 57,
                    "name": "Walter Walter Fun AG"
                },
                "share_percent": 0.0,
                "share_count": 0,
                "share_value": 0
            },
        ]
    }

This call returns all shareholders for the currently managed company. As of now only one company can be managed per user accounts. Shareholders cannot use the API to call for their shareholder data.
