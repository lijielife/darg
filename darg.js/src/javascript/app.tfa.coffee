# two factor auth
app = angular.module 'js.darg.app.tfa', ['js.darg.api','pascalprecht.translate','ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'TwoFactorAuthenticationController', ['$scope', '$http', '$window', '$filter', ($scope, $http, $window, $filter) ->
    $scope.submit = ->
        $('form')[0].submit()
        console.log('f')
]
