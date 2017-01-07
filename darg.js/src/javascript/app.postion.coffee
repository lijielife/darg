app = angular.module 'js.darg.app.position', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'PositionController', ['$scope', '$http', 'Position', ($scope, $http, Position) ->

    $scope.position = true
    $scope.errors = null

    $http.get('/services/rest/position/' + position_id).then (result) ->
        $scope.position = new Position(result.data)
]
