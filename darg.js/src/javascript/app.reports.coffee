app = angular.module 'js.darg.app.reports', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap', 'angularMoment']

# load moment locale
app.run (amMoment) ->
  amMoment.changeLocale 'de'
  return

# make amp timezone aware
angular.module('js.darg.app.reports').constant 'angularMomentConfig', timezone: 'Name of Timezone'

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'ReportsController', ['$scope', '$http', 'Shareholder', 'Report', ($scope, $http, Shareholder, Report) ->

    $scope.transactions_download_params = {}
    $scope.securities = []
    $scope.show_transaction_form = false
    $scope.enable_transaction_download = false
    $scope.transaction_download_url = ''

    # captable
    $scope.captable_orderings = [
        {title: gettext('Last Name'), value: 'get_full_name'},
        {title: gettext('Last Name (descending)'), value: 'get_full_name_desc'},
        {title: gettext('Share Count'), value: 'share_count'},
        {title: gettext('Share Count (descending)'), value: 'share_count_desc'},
        {title: gettext('Shareholder Number'), value: 'number'},
        {title: gettext('Shareholder Number (descending)'), value: 'number_desc'},
        {title: gettext('Share Percent Ownership'), value: 'share_percent'},
        {title: gettext('Share Percent Ownership (descending)'), value: 'share_percent_desc'},
        {title: gettext('Email'), value: 'user__email'},
        {title: gettext('Email desc'), value: 'user__email_desc'},
        {title: gettext('Capital based on face value'), value: 'cumulated_face_value'},
        {title: gettext('Capital based on face value desc'), value: 'cumulated_face_value_desc'},
        {title: gettext('Postal Code'), value: 'user__userprofile__postal_code'},
        {title: gettext('Postal Code desc'), value: 'user__user_profile__postal_code_desc'},
    ]
    $scope.report_types = [
        {title: gettext('Active Shareholders'), value: 'captable'},
        {title: gettext('Assembly Participation'), value: 'assembly_participation'},
        {title: gettext('Address data of all shareholders'), value: 'address_data'},
        {title: gettext('Printed Certificates'), value: 'certificates'},
        {title: gettext('Vested Shares'), value: 'vested_shares'},
    ]
    $scope.last_captable_report = undefined

    # --- dynamic props
    # transaction download url
    $scope.$watchCollection 'transactions_download_params', (transactions_download_params)->
        if transactions_download_params.to && transactions_download_params.from && transactions_download_params.security
            $scope.enable_transaction_download = true
            $scope.transaction_download_url = '/company/'+company_id+'/download/transactions?from='+$scope.transactions_download_params.from.toISOString()+'&to='+$scope.transactions_download_params.to.toISOString()+'&security='+$scope.transactions_download_params.security.pk

    # --- LOGIC
    $scope.add_captable_report = ->
        # previous report existing
        if $scope.last_captable_report.pk
            delete $scope.last_captable_report.pk

        # preprocess ordering
        $scope.last_captable_report.order_by = $scope.last_captable_report.order_by.value
        $scope.last_captable_report.report_type = $scope.last_captable_report.report_type.value
        $scope.last_captable_report.report_at = $scope.last_captable_report.report_at.toISOString().substring(0, 10)
        # save
        $scope.captable_loading = true
        $scope.last_captable_report.$save().then (result) ->
            $scope.last_captable_report = new Report($scope.get_report_from_api_result({data: results: [result]}))
            $scope.captable_loading=false
        , (rejection) ->
            $scope.captable_loading=false
            Raven.captureMessage('report creation error: ' + rejection.statusText, {
                level: 'error',
                extra: { rejection: rejection },
            })

    $scope.get_all_securities = ->
        $http.get('/services/rest/security').then (result) ->
            $scope.securities = result.data.results
        , (rejection) ->
            Raven.captureMessage('security loading error: ' + rejection.statusText, {
                level: 'error',
                extra: { rejection: rejection },
            })
            

    $scope.get_captable_report = ->
        if $scope.last_captable_report
            params = {
                order_by: $scope.last_captable_report.order_by.value,
                report_type: $scope.last_captable_report.report_type.value,
                file_type: $scope.last_captable_report.file_type,
                limit: 1,
                report_at: $scope.last_captable_report.report_at
            }
        else
            params = {}
        $scope.captable_loading = true
        $http.get('/services/rest/report', {params:params}).then (result) ->
            if result.data.results.length > 0
                $scope.last_captable_report = new Report($scope.get_report_from_api_result(result))
            else
                # if we don't have that report yet, make ablank one:
                params.order_by = $scope.lookup_ordering(params.order_by)
                params.report_type = $scope.lookup_report_type(params.report_type)
                # set default if there is nothing at all
                if not $scope.last_captable_report
                    $scope.last_captable_report = new Report({order_by: $scope.captable_orderings[6], file_type:'PDF', report_type: $scope.report_types[0], report_at: new Date()})
            $scope.captable_loading=false
        , (rejection) ->
            $scope.captable_loading=false
            Raven.captureMessage('report loading error: ' + rejection.statusText, {
                level: 'error',
                extra: { rejection: rejection },
            })

    $scope.get_report_from_api_result = (result) ->
        report = result.data.results[0]
        report.order_by = $scope.lookup_ordering(result.data.results[0].order_by)
        report.report_type = $scope.lookup_report_type(result.data.results[0].report_type)
        report.report_at = new Date(result.data.results[0].report_at)
        return report

    $scope.lookup_ordering = (order_by) ->
        orderings = $scope.captable_orderings.filter (obj) ->
            return obj.value == order_by
        return orderings[0] 

    $scope.lookup_report_type = (report_type) ->
        report_types = $scope.report_types.filter (obj) ->
            return obj.value == report_type
        return report_types[0] 

    # --- INITIAL DATA
    $scope.get_all_securities()
    $scope.get_captable_report()

    # --- display toggles
    $scope.toggle_transaction_form = ->
        if $scope.show_transaction_form
            $scope.show_transaction_form = false
        else
            $scope.show_transaction_form = true

    # --- DATEPICKER
    $scope.datepicker1 = { opened: false }
    $scope.datepicker1.format = 'd. MMM yyyy'
    $scope.datepicker1.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.toggle_datepicker1 = ->
        $scope.datepicker1.opened = !$scope.datepicker1.opened

    $scope.datepicker2 = { opened: false }
    $scope.datepicker2.format = 'd. MMM yyyy'
    $scope.datepicker2.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.toggle_datepicker2 = ->
        $scope.datepicker2.opened = !$scope.datepicker2.opened

    $scope.datepicker3 = { opened: false }
    $scope.datepicker3.format = 'd. MMM yyyy'
    $scope.datepicker3.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.toggle_datepicker3 = ->
        $scope.datepicker3.opened = !$scope.datepicker3.opened

]

