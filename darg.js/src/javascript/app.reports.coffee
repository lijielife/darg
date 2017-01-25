app = angular.module 'js.darg.app.reports', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'ReportsController', ['$scope', '$http', 'Shareholder', ($scope, $http, Shareholder) ->

]

