app = angular.module 'js.darg.app.options', ['js.darg.api','pascalprecht.translate','ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'OptionsController', ['$scope', '$http', '$window', '$filter', 'OptionPlan', 'OptionTransaction', ($scope, $http, $window, $filter, OptionPlan, OptionTransaction) ->

    $scope.option_plans = []
    $scope.securities = []
    $scope.shareholders = []
    $scope.loading = true

    $scope.show_add_option_transaction = false
    $scope.show_add_option_plan = false
    $scope.newOptionPlan = new OptionPlan()
    $scope.newOptionPlan.board_approved_at = new Date()
    $scope.newOptionTransaction = new OptionTransaction()
    $scope.newOptionTransaction.bought_at = new Date()

    $scope.numberSegmentsAvailable = ''
    $scope.hasSecurityWithTrackNumbers = () ->
        s = $scope.securities.find((el) ->
            return el.track_numbers==true
        )
        if s != undefined
            return true

    $http.get('/services/rest/optionplan').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.option_plans.push item

    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            if item.user.userprofile.birthday
                item.user.userprofile.birthday = new Date(item.user.userprofile.birthday)
            $scope.shareholders.push item
    .finally =>
        $scope.loading = false

    $scope.add_option_plan = ->
        if $scope.newOptionPlan.board_approved_at
            date = $scope.newOptionPlan.board_approved_at
            # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.newOptionPlan.board_approved_at = date.toISOString().substring(0, 10)
        $scope.newOptionPlan.$save().then (result) ->
            $scope.option_plans.push result
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
            $scope.newOptionPlan.board_approved_at = d

    $scope.add_option_transaction = ->
        # replace optionplan obj by hyperlinked url
        if $scope.newOptionTransaction.option_plan
            p = $scope.newOptionTransaction.option_plan
            $scope.newOptionTransaction.option_plan = $scope.newOptionTransaction.option_plan.url
        if $scope.newOptionTransaction.bought_at
            date = $scope.newOptionTransaction.bought_at
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.newOptionTransaction.bought_at = date.toISOString().substring(0, 10)
        $scope.newOptionTransaction.$save().then (result) ->
            $scope._reload_option_plans()
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionTransaction = new OptionPlan()
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
            $scope.newOptionTransaction.bought_at = d
            $scope.newOptionTransaction.option_plan = p

    $scope._reload_option_plans = () ->
        $scope.option_plans = []
        $http.get('/services/rest/optionplan').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.option_plans.push item

    $scope.delete_option_transaction = (option_transaction) ->
        $http.delete('/services/rest/optiontransaction/'+option_transaction.pk).then (result) ->
            $scope._reload_option_plans()

    $scope.confirm_option_transaction = (option_transaction) ->
        $http.post('/services/rest/optiontransaction/'+option_transaction.pk+'/confirm').then (result) ->
            $scope._reload_option_plans()

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
                company_shareholder_id = $filter('filter')($scope.shareholders, {is_company: true}, true)[0].pk
                url = '/services/rest/shareholders/' + company_shareholder_id.toString() + '/number_segments'
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
        if $scope.newOptionTransaction.seller && $scope.newOptionTransaction.option_plan
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
