app = angular.module 'js.darg.app.company', ['js.darg.api', 'xeditable', 'ngFileUpload', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'CompanyController', ['$scope', '$http', '$window', 'Company', 'Country', 'Operator', 'Upload', 'Security', '$timeout', ($scope, $http, $window, Company, Country, Operator, Upload, Security, $timeout) ->

    $scope.operators = []
    $scope.company = null
    $scope.errors = null
    $scope.show_add_operator_form = false

    $scope.file = null
    $scope.logo_success = false
    $scope.logo_errors = false
    $scope.loading = false

    $scope.newOperator = new Operator()

    $http.get('/services/rest/company/' + company_id).then (result) ->
        $scope.company = new Company(result.data)
        $scope.company.founded_at = new Date($scope.company.founded_at)
        if $scope.company.statement_sending_date
            $scope.company.statement_sending_date = new Date(
                $scope.company.statement_sending_date)
        if $scope.company.country
            $http.get($scope.company.country).then (result1) ->
                $scope.company.country = result1.data

    $http.get('/services/rest/country').then (result) ->
        $scope.countries = result.data.results

    $http.get('/services/rest/operators').then (result) ->
        $scope.operators = result.data.results

    $scope.toggle_add_operator_form = () ->
        if $scope.show_add_operator_form
            $scope.show_add_operator_form = false
        else
            $scope.show_add_operator_form = true

    $scope.delete_operator = (pk) ->
        $http.delete('/services/rest/operators/'+pk)
        .then ->
            $http.get('/services/rest/operators').then (result) ->
                $scope.operators = result.data.results

    $scope.add_operator = () ->
        $scope.newOperator.company = $scope.company.url
        $scope.newOperator.$save().then (result) ->
            $http.get('/services/rest/operators').then (result) ->
                $scope.operators = result.data.results
        .then ->
            # reset form
            $scope.newOperator = new Operator()
        .then ->
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('add operator form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    # save security. used esp. for its segments
    $scope.edit_security = (security) ->
        sec = new Security(security)
        sec.$update().then (result) ->
            i = $scope.company.security_set.indexOf(security)
            $scope.company.security_set[i] = result
        , (rejection) ->
            return rejection.data.number_segments[0]

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_company = () ->
        if $scope.company.country
            $scope.company.country = $scope.company.country.url
        if $scope.company.founded_at
            $scope.company.founded_at = $scope.company.founded_at.toISOString().substring(0, 10)
        if $scope.company.statement_sending_date
            $scope.company.statement_sending_date = $scope.company.statement_sending_date.toISOString().substring(0, 10)
            
        $scope.company.$update().then (result) ->
            result.founded_at = new Date(result.founded_at)
            if (result.statement_sending_date)
                result.statement_sending_date = new Date(result.statement_sending_date)
            $scope.company = new Company(result)
            # refetch country data
            $http.get($scope.company.country).then (result1) ->
                $scope.company.country = result1.data

        .then ->
            # Reset our editor to a new blank post
            #$scope.company = new Company()
            undefined
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.company.founded_at = new Date($scope.company.founded_at)
            $scope.errors = rejection.data
            Raven.captureMessage('edit corp form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    # logo upload
    $scope.$watch 'files', ->
      $scope.upload $scope.files
      return
    $scope.$watch 'file', ->
      if $scope.file != null
        $scope.files = [ $scope.file ]
      return

    $scope.upload = (files) ->
      if files and files.length
        $scope.loading = true
        i = 0
        while i < files.length
          file = files[i]
          if !file.$error
            # prepare data
            payload = $scope.company
            payload.founded_at = $scope.company.founded_at.toISOString().substring(0, 10)
            payload.logo = file
            Upload.upload(
              url: '/services/rest/company/'+company_id+'/upload'
              data: payload
              objectKey: '.k').then ((response) ->
                $timeout ->
                  company = new Company(response.data)
                  company.founded_at = new Date(company.founded_at)
                  company.statement_sending_date = new Date(company.statement_sending_date)
                  $scope.company = company
                  $scope.logo_success = true
                  $scope.logo_errors = false
                  return
                $timeout(() ->
                  $scope.logo_success = false
                  $scope.loading = false
                , 3000)
              ), ((response) ->
                $timeout ->
                  $scope.logo_errors = response.data
                  $scope.loading = false
              ), (evt) ->
                Raven.captureException(evt, {
                    level: 'warning',
                })
                return
              return

    # --- DATEPICKER
    $scope.datepicker = { opened: false }
    $scope.datepicker.format = 'd.MM.yy'
    $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker = ->
        $scope.datepicker.opened = true

    # --- company reset form
    $scope.confirm_company_reset = () ->
        $scope.errors = []
        if $scope.confirmCompanyText == gettext('DELETE')
            $scope.company.$delete().then () ->
                $('#companyResetModal').modal('hide')
                # track delete
                if !_.isUndefined(window.ga)
                    ga 'send', 'event', 'click', 'delete', 'company'
                $window.location.href = '/start/' 
        else
            label = gettext('Input')
            $scope.errors = {}
            $scope.errors[label] = [gettext('Please enter DELETE')]
]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
