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
    $scope.search_params = {'query': null, 'ordering': null, 'ordering_reverse': null}
    $scope.ordering_options = [
        {'name': gettext('Email'), 'value': 'user__email'},
        {'name': gettext('Shareholder Number'), 'value': 'number'},
        {'name': gettext('Last Name'), 'value': 'user__last_name'},
        # {'name': gettext('Clear'), 'value': null},
    ]

    # pagination:
    $scope.optionholder_next = false
    $scope.optionholder_previous = false
    $scope.optionholder_total = 0
    $scope.optionholder_current = 0
    $scope.optionholder_current_range = ''

    # search
    $scope.optionholder_search_params = {'query': null, 'ordering': null, 'ordering_reverse': null}
    $scope.optionholder_ordering_options = [
        {'name': gettext('Email'), 'value': 'user__email'},
        {'name': gettext('Shareholder Number'), 'value': 'number'},
        {'name': gettext('Last Name'), 'value': 'user__last_name'},
    ]

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
        #$scope.search_params.query = null

    $scope.optionholder_reset_search_params = ->
        $scope.optionholder_current = null
        $scope.optionholder_previous = null
        $scope.optionholder_next = null
        $scope.option_holders = []
        #$scope.search_params.query = null

    $scope.load_option_holders = (company_pk) ->
        $http.get('/services/rest/shareholders/option_holder?company='+company_pk).then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.option_holders.push item
            if result.data.next
                $scope.optionholder_next = result.data.next
            if result.data.previous
                $scope.optionholder_previous = result.data.previous
            if result.data.count
                $scope.optionholder_total=result.data.count
            if result.data.current
                $scope.optionholder_current=result.data.current

    $scope.load_all_shareholders = ->
        # FIXME - its not company specific
        $scope.reset_search_params()
        $scope.search_params.query = null
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
                # fetch option holders for this company
                $scope.load_option_holders(result1.data.pk)
        # update option holders if we have the company id
        if $scope.user.operator_set.length > 0 && $scope.user.operator_set[0].company.pk
           $scope.load_option_holders($scope.user.operator_set[0].company.pk)

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

    $scope.$watchCollection 'optionholder_current', (optionholder_current)->
        start = ($scope.optionholder_current - 1) * 20
        end = Math.min($scope.optionholder_current * 20, $scope.optionholder_total)
        $scope.optionholder_current_range = start.toString() + '-' + end.toString()

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

    $scope.optionholder_next_page = ->
        if $scope.optionholder_next
            $http.get($scope.optionholder_next).then (result) ->
                $scope.optionholder_reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.option_holders.push item
                if result.data.next
                    $scope.optionholder_next = result.data.next
                else
                    $scope.optionholder_next = false
                if result.data.previous
                    $scope.optionholder_previous = result.data.previous
                else
                    $scope.optionholder_previous = false
                if result.data.count
                    $scope.optionholder_total=result.data.count
                if result.data.current
                    $scope.optionholder_current=result.data.current

    $scope.optionholder_previous_page = ->
        if $scope.optionholder_previous
            $http.get($scope.optionholder_previous).then (result) ->
                $scope.optionholder_reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.option_holders.push item
                if result.data.next
                    $scope.optionholder_next = result.data.next
                else
                    $scope.optionholder_next = false
                if result.data.previous
                    $scope.optionholder_previous = result.data.previous
                else
                    $scope.optionholder_previous = false
                if result.data.count
                    $scope.optionholder_total=result.data.count
                if result.data.current
                    $scope.optionholder_current=result.data.current

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

        $http.get('/services/rest/shareholders?' + paramss).then (result) ->
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
            $scope.search_params.query = params.search

    $scope.optionholder_search = ->
        # FIXME - its not company specific
        # respect ordering and search
        params = {}
        params.company = $scope.user.operator_set[0].company.pk
        if $scope.optionholder_search_params.query
            params.search = $scope.optionholder_search_params.query
        if $scope.optionholder_search_params.ordering
            params.ordering = $scope.optionholder_search_params.ordering
        paramss = $.param(params)

        $http.get('/services/rest/shareholders/option_holder?' + paramss).then (result) ->
            $scope.optionholder_reset_search_params()
            angular.forEach result.data.results, (item) ->
                $scope.option_holders.push item
            if result.data.next
                $scope.optionholder_next = result.data.next
            if result.data.previous
                $scope.optionholder_previous = result.data.previous
            if result.data.count
                $scope.optionholder_total=result.data.count
            if result.data.current
                $scope.optionholder_current=result.data.current
            $scope.optionholder_search_params.query = params.search

    # --- FORMS
    $scope.add_company = ->
        $scope.errors = null
        $scope.newCompany.$save().then (result) ->
            $http.get('/services/rest/user').then (result) ->
                $scope.user = result.data.results[0]
                # loop over ops and fetch corp data
                angular.forEach $scope.user.operator_set, (item, key) ->
                    $http.get(item.company).then (result1) ->
                        $scope.user.operator_set[key].company = result1.data
            .then ->
                # load shs and option holders
                $scope.load_all_shareholders()

        .then ->
            # Reset our editor to a new blank post
            $scope.company = new Company()
            $window.ga('send', 'event', 'form-send', 'add-company')
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('add corp form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    $scope.add_shareholder = ->
        $scope.errors = null
        $scope.newShareholder.$save().then (result) ->
            $scope.shareholders.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newShareholder = new Shareholder()
            $scope.shareholder_added_success = true
            $scope.show_add_shareholder = false
            $timeout ->
                $scope.shareholder_added_success = false
            , 30000
        .then ->
            # Clear any errors
            $scope.errors = null
            $window.ga('send', 'event', 'form-send', 'add-shareholder')
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('add shareholder form error: ' + rejection.statusText, {
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
    $scope.toggle_datepicker = ->
        $scope.datepicker.opened = !$scope.datepicker.opened
        return false
]
