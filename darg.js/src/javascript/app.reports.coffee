app = angular.module 'js.darg.app.reports', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'ReportsController', ['$scope', '$http', 'Shareholder', ($scope, $http, Shareholder) ->

    $scope.transactions_download_params = {}
    $scope.securities = []
    $scope.show_transaction_form = false
    $scope.enable_transaction_download = false
    $scope.transaction_download_url = ''

    # captable
    $scope.show_captable_form = false
    $scope.captable_orderings = [
        {title: gettext('Last Name'), value: 'user__last_name'},
        {title: gettext('Last Name (descending)'), value: 'user__last_name_desc'},
        {title: gettext('Share Count'), value: 'share_count'},
        {title: gettext('Share Count (descending)'), value: 'share_count_desc'},
        {title: gettext('Shareholder Number'), value: 'number'},
        {title: gettext('Shareholder Number (descending)'), value: 'number_desc'},
        {title: gettext('Share Percent Ownership'), value: 'share_percent'},
        {title: gettext('Share Percent Ownership (descending)'), value: 'share_percent_desc'},
    ]
    $scope.captable_report = {ordering: $scope.captable_orderings[6]}
    $scope.captable_csv_url = ''
    $scope.captable_pdf_url = ''

    # intial data
    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    # --- dynamic props
    # transaction download url
    $scope.$watchCollection 'transactions_download_params', (transactions_download_params)->
        if transactions_download_params.to && transactions_download_params.from && transactions_download_params.security
            $scope.enable_transaction_download = true
            $scope.transaction_download_url = '/company/'+company_id+'/download/transactions?from='+$scope.transactions_download_params.from.toISOString()+'&to='+$scope.transactions_download_params.to.toISOString()+'&security='+$scope.transactions_download_params.security.pk

    # transaction download url
    $scope.$watchCollection 'captable_report', (captable_report)->
        ext = ''
        if captable_report.ordering
            ext = '?ordering=' + captable_report.ordering.value
        $scope.captable_csv_url = '/company/'+company_id+'/download/pdf' + ext
        $scope.captable_pdf_url =  '/company/'+company_id+'/download/csv' + ext

    # --- display toggles
    $scope.toggle_transaction_form = ->
        if $scope.show_transaction_form
            $scope.show_transaction_form = false
        else
            $scope.show_transaction_form = true

    $scope.toggle_captable_form = ->
        if $scope.show_captable_form
            $scope.show_captable_form = false
        else
            $scope.show_captable_form = true

    # --- DATEPICKER
    $scope.datepicker1 = { opened: false }
    $scope.datepicker1.format = 'd. MMM yyyy'
    $scope.datepicker1.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.toggle_datepicker1 = ->
        $scope.datepicker1.opened = !$scope.datepicker1.opened

    $scope.datepicker2 = { opened: false }
    $scope.datepicker2.format = 'd. MMM yyyy'
    $scope.datepicker2.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.toggle_datepicker2 = ->
        $scope.datepicker2.opened = !$scope.datepicker2.opened

]

