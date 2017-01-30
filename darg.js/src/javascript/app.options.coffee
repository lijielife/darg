app = angular.module 'js.darg.app.options', ['js.darg.api','pascalprecht.translate','ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'OptionsController', ['$scope', '$http', '$window', '$filter', 'OptionPlan', 'OptionTransaction', ($scope, $http, $window, $filter, OptionPlan, OptionTransaction) ->

    $scope.option_plans = []
    $scope.optiontransactions = []
    $scope.securities = []
    $scope.loading = true

    $scope.show_add_option_transaction = false
    $scope.show_add_option_plan = false
    $scope.show_optional_fields = false
    $scope.newOptionPlan = new OptionPlan()
    $scope.newOptionPlan.board_approved_at = new Date()
    $scope.newOptionTransaction = new OptionTransaction()
    $scope.newOptionTransaction.bought_at = new Date()
    $scope.depot_types = [
        {name: gettext('Sperrdepot'), value: '2'},
        {name: gettext('Zertifikatsdepot'), value: '0'},
        {name: gettext('Gesellschaftsdepot'), value: '1'},
    ]

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
        $scope.optiontransactions = []
        $scope.option_plans = []
        #$scope.search_params.query = null

    $scope.load_all = ->
        # FIXME - its not company specific
        $scope.reset_search_params()
        $scope.search_params.query = null

        $http.get('/services/rest/optiontransaction').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.optiontransactions.push item
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
        .finally ->
            $scope.loading = false

        $http.get('/services/rest/optionplan').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.option_plans.push item

    $scope.load_all()

    # used inside the add transaction form
    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    # --- PAGINATION
    $scope.next_page = ->
        if $scope.next
            $http.get($scope.next).then (result) ->
                $scope.reset_search_params()
                angular.forEach result.data.results, (item) ->
                    $scope.optiontransactions.push item
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
                    $scope.optiontransactions.push item
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
    $scope.search_shareholders = (term) ->
        paramss = {search: term}
        $http.get('/services/rest/shareholders', {params: paramss}).then (response) ->
            response.data.results.map (item) ->
                item

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

        $http.get('/services/rest/optiontransaction?' + paramss).then (result) ->
            $scope.reset_search_params()
            angular.forEach result.data.results, (item) ->
                $scope.optiontransactions.push item
            if result.data.next
                $scope.next = result.data.next
            if result.data.previous
                $scope.previous = result.data.previous
            if result.data.count
                $scope.total=result.data.count
            if result.data.current
                $scope.current=result.data.current
            $scope.search_params.query = params.search

    # -- LOGIC
    $scope.add_option_plan = ->
        if $scope.newOptionPlan.board_approved_at
            date = $scope.newOptionPlan.board_approved_at
            # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.newOptionPlan.board_approved_at = date.toISOString().substring(0, 10)

        $scope.newOptionPlan.$save().then (result) ->
            $scope.load_all()
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionPlan = new OptionPlan()
            $scope.show_add_option_plan = false
        .then ->
            # Clear any errors
            $scope.errors = null
            $window.ga('send', 'event', 'form-send', 'add-optionplan')
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })
            if date
                $scope.newOptionPlan.board_approved_at = date

    $scope.add_option_transaction = ->
        # replace optionplan obj by hyperlinked url
        if $scope.newOptionTransaction.option_plan
            p = $scope.newOptionTransaction.option_plan
        if $scope.newOptionTransaction.bought_at
            date = $scope.newOptionTransaction.bought_at
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.newOptionTransaction.bought_at = date.toISOString().substring(0, 10)
        # replace legal type obj by str
        if $scope.newOptionTransaction.depot_type
            $scope.newOptionTransaction.depot_type = $scope.newOptionTransaction.depot_type.value

        # now save:
        $scope.newOptionTransaction.$save().then (result) ->
            $scope.load_all()
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionTransaction = new OptionTransaction()
            $scope.show_add_option_transaction = false
        .then ->
            # Clear any errors
            $scope.errors = null
            $window.ga('send', 'event', 'form-send', 'add-option-transaction')
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })
            $scope.newOptionTransaction.bought_at = date
            $scope.newOptionTransaction.option_plan = p

    $scope.delete_option_transaction = (option_transaction) ->
        $http.delete('/services/rest/optiontransaction/'+option_transaction.pk).then (result) ->
            $scope.load_all()

    $scope.confirm_option_transaction = (option_transaction) ->
        $http.post('/services/rest/optiontransaction/'+option_transaction.pk+'/confirm').then (result) ->
            $scope.load_all()

    $scope.show_add_option_plan_form = ->
        $scope.show_add_option_plan = true
        $scope.show_add_option_transaction = false
        $scope.newOptionPlan = new OptionPlan()

    $scope.show_add_option_transaction_form = ->
        $scope.show_add_option_transaction = true
        $scope.show_add_option_plan = false
        $scope.newOptionTransaction = new OptionTransaction()

    $scope.hide_form = ->
        $scope.show_add_option_plan = false
        $scope.show_add_option_transaction = false
        $scope.newOptionPlan = new OptionPlan()
        $scope.newOptionTransaction = new OptionTransaction()

    $scope.show_available_number_segments_for_new_option_plan = ->
        if $scope.newOptionPlan.security
            if $scope.newOptionPlan.security.track_numbers
                url = '/services/rest/shareholders/company_number_segments'
                if $scope.newOptionPlan.board_approved_at
                    url = url + '?date=' + $scope.newOptionPlan.board_approved_at.toISOString()
                $http.get(url).then (result) ->
                    if $scope.newOptionPlan.security.pk of result.data and result.data[$scope.newOptionPlan.security.pk].length > 0
           	            $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data[$scope.newOptionPlan.security.pk]
                    else
                        $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: None')
            else
                $scope.numberSegmentsAvailable = ''

    $scope.show_available_number_segments_for_new_option_transaction = ->
        if $scope.newOptionTransaction.seller && $scope.newOptionTransaction.option_plan && $scope.newOptionTransaction.option_plan.security.track_numbers
            op_pk = $scope.newOptionTransaction.option_plan.pk.toString()
            sh_pk = $scope.newOptionTransaction.seller.pk.toString()
            url = '/services/rest/optionplan/' + op_pk + '/number_segments/' + sh_pk
            if $scope.newOptionTransaction.bought_at
                url = url + '?date=' + $scope.newOptionTransaction.bought_at.toISOString()
            $http.get(url).then (result) ->
                if result.data and result.data.length > 0
                    $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data
                else
                    $scope.numberSegmentsAvailable = gettext('No security segments available for option plan on selected date or now.')

    $scope.toggle_optional_fields = ->
        if $scope.show_optional_fields
            $scope.show_optional_fields = false
        else
            $scope.show_optional_fields = true

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

    # --- LINK
    $scope.goto_option = (option_id) ->
        window.location = "/options/"+option_id+"/"

]

app.directive 'stringToNumber', ->
  {
    require: 'ngModel'
    link: (scope, element, attrs, ngModel) ->
      ngModel.$parsers.push (value) ->
        '' + value
      ngModel.$formatters.push (value) ->
        parseFloat value
      return

  }
