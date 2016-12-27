app = angular.module 'js.darg.app.start', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'StartController', ['$scope', '$window', '$http', 'CompanyAdd', 'Shareholder', 'User', 'Company', '$timeout', ($scope, $window, $http, CompanyAdd, Shareholder, User, Company, $timeout) ->

    # from server
    $scope.shareholders = []
    $scope.option_holders = []
    $scope.user = []
    $scope.total_shares = 0
    $scope.loading = true
    $scope.shareholder_added_success = false

    # pagination:
    $scope.next = false
    $scope.previous = false
    $scope.total = 0
    $scope.current = 0
    $scope.current_range = ''

    # search
    $scope.search = {'query': null}

    $scope.show_add_shareholder = false

    # empty form data
    $scope.newShareholder = new Shareholder()
    $scope.newCompany = new CompanyAdd()


    # --- INITIAL
    $scope.reset_search_params = ->
        $scope.current = null
        $scope.previous = null
        $scope.next = null
        $scope.shareholders = []
        #$scope.search.query = null

    $scope.load_all_shareholders = ->
        # FIXME - its not company specific
        $scope.reset_search_params()
        $scope.search.query = null
        $http.get('/services/rest/shareholders').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.shareholders.push item
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
    $scope.load_all_shareholders()
          

    $http.get('/services/rest/user').then (result) ->
        $scope.user = result.data.results[0]
        # loop over ops and fetch corp data
        angular.forEach $scope.user.operator_set, (item, key) ->
            # get company data
            $http.get(item.company).then (result1) ->
                $scope.user.operator_set[key].company = result1.data
                # fetch operators for this company
                $http.get('/services/rest/company/'+result1.data.pk+'/option_holder').then (result2) ->
                    angular.forEach result2.data.results, (item) ->
                        $scope.option_holders.push item

    .finally ->
        $scope.loading = false

    # --- Dynamic props
    $scope.$watchCollection 'shareholders', (shareholders)->
        $scope.total_shares = 0
        angular.forEach shareholders, (item) ->
            $scope.total_shares = item.share_count + $scope.total_shares

    $scope.$watchCollection 'current', (current)->
        start = ($scope.current - 1) * 20
        end = Math.min($scope.current * 20, $scope.total)
        $scope.current_range = start.toString() + '-' + end.toString()

    # --- PAGINATION
    $scope.next_page = ->
        if $scope.next
            $http.get($scope.next).then (result) ->
                $scope.reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.shareholders.push item
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
                    $scope.shareholders.push item
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
        query = $scope.search.query
        $http.get('/services/rest/shareholders?search=' + query).then (result) ->
            $scope.reset_search_params()
            angular.forEach result.data.results, (item) ->
                $scope.shareholders.push item
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
            $scope.search.query = query

    # --- FORMS
    $scope.add_company = ->
        $scope.newCompany.$save().then (result) ->
            $http.get('/services/rest/user').then (result) ->
                $scope.user = result.data.results[0]
                # loop over ops and fetch corp data
                angular.forEach $scope.user.operator_set, (item, key) ->
                    $http.get(item.company).then (result1) ->
                        $scope.user.operator_set[key].company = result1.data
                        # fetch operators for this company
                        $http.get('/services/rest/company/'+result1.data.pk+'/option_holder').then (result2) ->
                            angular.forEach result2.data.results, (item) ->
                                $scope.option_holders.push item

            $http.get('/services/rest/shareholders').then (result) ->
                angular.forEach result.data.results, (item) ->
                    $scope.shareholders.push item
        .then ->
            # Reset our editor to a new blank post
            $scope.company = new Company()
            $window.ga('send', 'event', 'form-send', 'add-company')
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    $scope.add_shareholder = ->
        $scope.newShareholder.$save().then (result) ->
            $scope.shareholders.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newShareholder = new Shareholder()
            $scope.shareholder_added_success = true
            $timeout ->
                $scope.shareholder_added_success = false
            , 30000
        .then ->
            # Clear any errors
            $scope.errors = null
            $window.ga('send', 'event', 'form-send', 'add-shareholder')
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })


    $scope.show_add_shareholder_form = ->
        $scope.show_add_shareholder = true

    $scope.hide_form = ->
        $scope.show_add_shareholder = false

    $scope.goto_shareholder = (shareholder_id) ->
        window.location = "/shareholder/"+shareholder_id+"/"


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
