.. role:: python(code)
   :language: python

Shareholder Statements
======================

das-aktienregister.ch features an auto-generated statement for shareholders of
companies that subscribed to an appropiate plan
(which has the 'shareholder_statements' feature enabled)

Statements will be sent to shareholder via email. The shareholder (user) can
also download the pdf file with a single-auth url provided in the email.
If the shareholder does not open the email in time (see Settings_), a physical
letter will be sent (if address provided) via a service (Pingen_)

Company operators can view statement reports in the frontend (submenu entry).

Shareholder users can view all their statements in the frontend as well
(but they don't have a login yet).


Settings
--------

:python:`SHAREHOLDER_STATEMENT_ROOT`
:python:`(os.path.join(SENDFILE_ROOT, 'shareholder', 'statements'))`

   root of statement pdf files;
   filepath is <user_id>/<company_id>/<year>/

:python:`SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_DAYS`
:python:`7`

   notification for company operators that shareholder statements will be
   generated and sent

:python:`SHAREHOLDER_STATEMENT_EMAIL_OPENED_DAYS`
:python:`7`

   days to watch if email was opened

:python:`SHAREHOLDER_STATMENT_LETTER_OFFSET_DAYS`
:python:`7`

   offset to send physical/postal letter to shareholders that didn't opened
   email (in time)

:python:`SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_DAYS`
:python:`14`

   notification for company operators that a report for shareholder statements
   is available

Tasks
-----

in shareholder.tasks

:python:`send_statement_generation_operator_notify()`

   send a notification to company operators that shareholder statements will be
   generated and sent

   uses ``MANDRILL_SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_TEMPLATE``
   if ``djrill`` is email backend

   **NOTE**: should be called periodically once a day

:python:`send_statement_report_operator_notify()`

   send a notification to company operators that a report for shareholder
   statements is available

   uses ``MANDRILL_SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_TEMPLATE``
   if ``djrill`` is email backend

   **NOTE**: should be called periodically once a day

:python:`generate_statements_report()`

   generate shareholder statement report and statements

   **NOTE**: should be called periodically once a day

:python:`send_statement_email(statement_id)`

   send email to user with shareholder statement

   uses ``MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE``
   if ``djrill`` is email backend

:python:`fetch_statement_email_opened_mandrill`

   try to fetch the "opened at" tracking via mandrill

   **NOTE**: should be called periodically once a day

:python:`send_statement_letter(statement_id)`

   send letter to statement user via service (pingen)

:python:`send_statement_letters()`

   send letter statements to all shareholder users, that did not downloaded
   the pdf file (in time)

   **NOTE**: should be called periodically once a day


Pingen
------

Letters to shareholders (who did not open the email in time) will be sent via
https://pingen.com (obviously, an API Token is required).

A simple wrapper for the API was implemented, that (for now) only supports
document upload.


Pingen Settings:
~~~~~~~~~~~~~~~~

:python:`PINGEN_API_TOKEN`
:python:`None`

   set this in local settings

:python:`PINGEN_SEND_ON_UPLOAD`
:python:`False`

   should the letter be immediately sent after upload
   (careful here when testing!)

:python:`PINGEN_SEND_COLOR`
:python:`2`

   0 = black/white, 1 = Color, 2 = Mixed (optimized)

:python:`PINGEN_API_URL`
:python:`'https://api.pingen.com'`

   api endpoint url

   **NOTE:** can't upload to stage api!

see pingen/conf.py for more options
