app = angular.module 'js.darg.app.positions', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'PositionsController', ['$scope', '$http', '$window', 'Position', 'Split', ($scope, $http, $window, Position, Split) ->
    $scope.positions = []
    $scope.shareholders = []
    $scope.securities = []

    $scope.show_add_position = false
    $scope.show_add_capital = false
    $scope.show_split_data = false
    $scope.show_split = false
    $scope.newPosition = new Position()
    $scope.newSplit = new Split()

    $scope.numberSegmentsAvailable = ''
    $scope.hasSecurityWithTrackNumbers = () ->
        s = $scope.securities.find((el) ->
            return el.track_numbers==true
        )
        if s != undefined
            return true
    $scope.positionsLoading = true
    $scope.addPositionLoading = false
    
    $http.get('/services/rest/position').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.positions.push item
        $scope.positionsLoading = false

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            if item.user.userprofile.birthday
                item.user.userprofile.birthday = new Date(item.user.userprofile.birthday)
            $scope.shareholders.push item

    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    $scope.add_position = ->
        $scope.addPositionLoading = true
        if $scope.newPosition.bought_at
            # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
            bought_at = $scope.newPosition.bought_at
            bought_at.setHours(bought_at.getHours() - bought_at.getTimezoneOffset() / 60)
            $scope.newPosition.bought_at = bought_at
        $scope.newPosition.$save().then (result) ->
            $scope.positions.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.show_add_position = false
            $scope.show_add_capital = false
            $scope.newPosition = new Position()
        .then ->
            # Clear any errors
            $scope.errors = null
            $window.ga('send', 'event', 'form-send', 'add-transaction')
            $scope.addPositionLoading = false
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })
            $scope.addPositionLoading = false

    $scope.delete_position = (position) ->
        $scope.positionsLoading = true
        $http.delete('/services/rest/position/'+position.pk).then (result) ->
            $scope.positions = []
            $http.get('/services/rest/position').then (result1) ->
                angular.forEach result1.data.results, (item) ->
                    $scope.positions.push item
            $scope.positionsLoading = false

    $scope.confirm_position = (position) ->
        $http.post('/services/rest/position/'+position.pk+'/confirm').then (result) ->
            $scope.positions = []
            $http.get('/services/rest/position').then (result1) ->
                angular.forEach result1.data.results, (item) ->
                    $scope.positions.push item
                $scope.positionsLoading = false

    $scope.add_split = ->
        # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
        execute_at = $scope.newSplit.execute_at
        execute_at.setHours(execute_at.getHours() - execute_at.getTimezoneOffset() / 60)
        $scope.newSplit.execute_at = execute_at
        $scope.newSplit.$save().then (result) ->
            $scope.positions = result.data
        .then ->
            $scope.newSplit = new Split()
        .then ->
            $scope.errors = null
            $scope.show_split = false
            $window.ga('send', 'event', 'form-send', 'add-split')
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    $scope.show_add_position_form = ->
        $scope.show_add_position = true
        $scope.show_add_capital = false
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.toggle_show_split_data = ->
        if $scope.show_split_data
            $scope.show_split_data = false
        else
            $scope.show_split_data = true

    $scope.show_add_capital_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = true
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.hide_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = false
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.show_split_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = false
        $scope.newSplit = new Split()
        $scope.show_split = true

    $scope.show_available_number_segments = ->
        if $scope.newPosition.security
            if $scope.newPosition.security.track_numbers and $scope.newPosition.seller
                url = '/services/rest/shareholders/' + $scope.newPosition.seller.pk.toString() + '/number_segments'
                if $scope.newPosition.bought_at
                    url = url + '?date=' + $scope.newPosition.bought_at.toISOString()
                $http.get(url).then (result) ->
                    if $scope.newPosition.security.pk of result.data and result.data[$scope.newPosition.security.pk].length > 0
           	            $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: ') + result.data[$scope.newPosition.security.pk]
                    else
                        $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: None')

    # --- DATEPICKER
    $scope.datepicker = { opened: false }
    $scope.datepicker.format = 'd. MMM yyyy'
    $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker = ->
        $scope.datepicker.opened = true


]
