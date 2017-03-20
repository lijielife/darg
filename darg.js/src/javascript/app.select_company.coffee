app = angular.module 'js.darg.app.select_company', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'SelectCompanyController', ['$scope', '$http', ($scope, $http) ->

]

