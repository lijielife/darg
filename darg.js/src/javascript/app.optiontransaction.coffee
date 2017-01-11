app = angular.module 'js.darg.app.optiontransaction', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'OptionTransactionController', ['$scope', '$http', 'OptionTransaction', ($scope, $http, OptionTransaction) ->

    $scope.optiontransaction = true

    $http.get('/services/rest/optiontransaction/' + optiontransaction_id).then (result) ->
        $scope.optiontransaction = new OptionTransaction(result.data)
]
