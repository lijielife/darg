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

    # pagination:
    $scope.next = false
    $scope.previous = false
    $scope.total = 0
    $scope.current = 0
    $scope.current_range = ''

    # search
    $scope.search_params = {'query': null, 'ordering': null, 'ordering_reverse': null}
    $scope.ordering_options = false

    $scope.numberSegmentsAvailable = ''
    $scope.hasSecurityWithTrackNumbers = () ->
        s = $scope.securities.find((el) ->
            return el.track_numbers==true
        )
        if s != undefined
            return true
    $scope.positionsLoading = true
    $scope.addPositionLoading = false


    # --- Dynamic props
    $scope.$watchCollection 'current', (current)->
        start = ($scope.current - 1) * 20
        end = Math.min($scope.current * 20, $scope.total)
        $scope.current_range = start.toString() + '-' + end.toString()
 

    # --- INITIAL
    $scope.reset_search_params = ->
        $scope.current = null
        $scope.previous = null
        $scope.next = null
        $scope.positions = []
        #$scope.search_params.query = null

    $scope.load_all_positions = ->
        # FIXME - its not company specific
        $scope.reset_search_params()
        $scope.search_params.query = null
        $http.get('/services/rest/position').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.positions.push item
            $scope.positionsLoading = false
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
    $scope.load_all_positions()

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            if item.user.userprofile.birthday
                item.user.userprofile.birthday = new Date(item.user.userprofile.birthday)
            $scope.shareholders.push item

    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    # --- PAGINATION
    $scope.next_page = ->
        if $scope.next
            $http.get($scope.next).then (result) ->
                $scope.reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.positions.push item
                if result.data.next
                    $scope.next = result.data.next
                else
                    $scope.next = false
                if result.data.previous
                    $scope.previous = result.data.previous
                else
                    $scope.previous = false
                if result.data.count
                    $scope.total=result.data.count
                if result.data.current
                    $scope.current=result.data.current

    $scope.previous_page = ->
        if $scope.previous
            $http.get($scope.previous).then (result) ->
                $scope.reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.positions.push item
                if result.data.next
                    $scope.next = result.data.next
                else
                    $scope.next = false
                if result.data.previous
                    $scope.previous = result.data.previous
                else
                    $scope.previous = false
                if result.data.count
                    $scope.total=result.data.count
                if result.data.current
                    $scope.current=result.data.current

    # --- SEARCH
    $scope.search = ->
        # FIXME - its not company specific
        # respect ordering and search
        params = {}
        if $scope.search_params.query
            params.search = $scope.search_params.query
        if $scope.search_params.ordering
            params.ordering = $scope.search_params.ordering
        paramss = $.param(params)
        console.log(params)

        $http.get('/services/rest/position?' + paramss).then (result) ->
            $scope.reset_search_params()
            angular.forEach result.data.results, (item) ->
                $scope.positions.push item
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
            $scope.search_params.query = params.query

    # --- LOGIC
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
