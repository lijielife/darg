app = angular.module 'js.darg.app.position', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'PositionController', ['$scope', '$http', 'Position', ($scope, $http, Position) ->

    $scope.position = null
    $scope.errors = null

    $scope.load_position    = ->
        $http.get('/services/rest/position/' + position_id).then (result) ->
            $scope.position = new Position(result.data)

    # --- INIT
    $scope.load_position()

    # --- LOGIC
    # invalidate certificate
    $scope.invalidate_certificate = ->
        if $scope.position
            $scope.position.$invalidate({id: position_id}).then (result) ->
                $scope.position = result
            , (rejection) ->
                Raven.captureMessage('invalidate certificate error: ' + rejection.statusText, {
                    level: 'warning',
                    extra: { rejection: rejection },
                })
]
