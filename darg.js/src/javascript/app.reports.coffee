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

    # intial data
    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    # dynamic props
    $scope.$watchCollection 'transactions_download_params', (transactions_download_params)->
        if transactions_download_params.to && transactions_download_params.from && transactions_download_params.security
            $scope.enable_transaction_download = true
            $scope.transaction_download_url = '/company/'+company_id+'/download/transactions?from='+$scope.transactions_download_params.from.toISOString()+'&to='+$scope.transactions_download_params.to.toISOString()+'&security='+$scope.transactions_download_params.security.pk

    $scope.toggle_transaction_form = ->
        if $scope.show_transaction_form
            $scope.show_transaction_form = false
        else
            $scope.show_transaction_form = true

    # --- DATEPICKER
    $scope.datepicker1 = { opened: false }
    $scope.datepicker1.format = 'd. MMM yyyy'
    $scope.datepicker1.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker1 = ->
        $scope.datepicker1.opened = true

    $scope.datepicker2 = { opened: false }
    $scope.datepicker2.format = 'd. MMM yyyy'
    $scope.datepicker2.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker2 = ->
        $scope.datepicker2.opened = true

]

