app = angular.module 'js.darg.app.shareholder', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'ShareholderController', ['$scope', '$http', 'Shareholder', ($scope, $http, Shareholder) ->

    $scope.shareholder = true
    $scope.countries = []
    $scope.languages = []
    $scope.errors = null

    $scope.legal_types = [
        {name: gettext('Human Being'), value: 'H'},
        {name: gettext('Corporate'), value: 'C'},
    ]

    $scope.mailing_types = [
        {name: gettext('Not deliverable'), value: '0'},
        {name: gettext('Postal Mail'), value: '1'},
        {name: gettext('via Email'), value: '2'},
    ]

    $http.get('/services/rest/language').then (result_lang) ->
            $scope.languages = result_lang.data

        $http.get('/services/rest/shareholders/' + shareholder_id).then (result) ->
            # convert birthay to JS obj
            if result.data.user.userprofile.birthday != null
                result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday)

            # create Shareholder JS obj
            $scope.shareholder = new Shareholder(result.data)

            # fetch country/nationality hyperlinked obj
            if $scope.shareholder.user.userprofile.country
                $http.get($scope.shareholder.user.userprofile.country).then (result1) ->
                    $scope.shareholder.user.userprofile.country = result1.data
            if $scope.shareholder.user.userprofile.nationality
                $http.get($scope.shareholder.user.userprofile.nationality).then (result1) ->
                    $scope.shareholder.user.userprofile.nationality = result1.data
            # assign legal type obj
            legal_type = $scope.legal_types.filter (obj) ->
                return obj.value == $scope.shareholder.user.userprofile.legal_type
            $scope.shareholder.user.userprofile.legal_type = legal_type[0]
            # assign mailing type obj
            mailing_type = $scope.mailing_types.filter (obj) ->
                return obj.value == $scope.shareholder.mailing_type
            $scope.shareholder.mailing_type = mailing_type[0]
            if $scope.shareholder.user.userprofile.language
                language = $scope.languages.filter (obj) ->
                    return obj.iso == $scope.shareholder.user.userprofile.language
                $scope.shareholder.user.userprofile.language = language[0]

    $http.get('/services/rest/country').then (result) ->
            $scope.countries = result.data.results

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_shareholder = () ->
        # change birthday to rest format
        if $scope.shareholder.user.userprofile.birthday
            # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
            date = $scope.shareholder.user.userprofile.birthday
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.shareholder.user.userprofile.birthday = date
        # replace country obj by hyperlink
        if $scope.shareholder.user.userprofile.country
            $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url
        # replace nationality obj by hyperlink
        if $scope.shareholder.user.userprofile.nationality
            $scope.shareholder.user.userprofile.nationality = $scope.shareholder.user.userprofile.nationality.url
        # replace language obj by hyperlink
        if $scope.shareholder.user.userprofile.language
            $scope.shareholder.user.userprofile.language = $scope.shareholder.user.userprofile.language.iso
        # replace legal type obj by str
        if $scope.shareholder.user.userprofile.legal_type
            $scope.shareholder.user.userprofile.legal_type = $scope.shareholder.user.userprofile.legal_type.value
        # replace mailing type obj by str
        if $scope.shareholder.mailing_type
            $scope.shareholder.mailing_type = $scope.shareholder.mailing_type.value
        # --- SAVE
        $scope.shareholder.$update().then (result) ->
            if result.user.userprofile.birthday != null
                result.user.userprofile.birthday = new Date(result.user.userprofile.birthday)
            $scope.shareholder = new Shareholder(result)
            # adjust local data so it can be properly displayed
            if $scope.shareholder.user.userprofile.country
                $http.get($scope.shareholder.user.userprofile.country).then (result1) ->
                    $scope.shareholder.user.userprofile.country = result1.data
            if $scope.shareholder.user.userprofile.nationality
                $http.get($scope.shareholder.user.userprofile.nationality).then (result1) ->
                    $scope.shareholder.user.userprofile.nationality = result1.data
            if $scope.shareholder.user.userprofile.legal_type
                legal_type = $scope.legal_types.filter (obj) ->
                    return obj.value == $scope.shareholder.user.userprofile.legal_type
                $scope.shareholder.user.userprofile.legal_type = legal_type[0]
            if $scope.shareholder.user.userprofile.language
                language = $scope.languages.filter (obj) ->
                    return obj.iso == $scope.shareholder.user.userprofile.language
                $scope.shareholder.user.userprofile.language = language[0]
        .then ->
            # Reset our editor to a new blank post
            #$scope.company = new Company()
            undefined
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('edit shareholder form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    # --- DISPLAY
    $scope.toggle_locked_positions = (id) ->

        if $scope.locked_positions_security ==  id
            $scope.locked_positions_security = null
        else
            $scope.locked_positions_security = id


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

]

# FIXME make global for all controllers
app.filter 'percentage', [
  '$filter'
  ($filter) ->
    (input, decimals) ->
      $filter('number')(input * 100, decimals) + '%'
]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
