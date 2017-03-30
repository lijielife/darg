app = angular.module 'js.darg.api', ['ngResource']

app.factory 'Shareholder', ['$resource', ($resource) ->
    $resource('/services/rest/shareholders/:id', {id: '@pk'} , update: method: 'PUT')
]

app.factory 'Security', ['$resource', ($resource) ->
    $resource('/services/rest/security/:id', {id: '@pk'} , update: method: 'PUT')
]
app.factory 'CompanyAdd', ['$resource', ($resource) ->
    $resource '/services/rest/company/add/'
]

app.factory 'Company', ['$resource', ($resource) ->
    $resource('/services/rest/company/:id', {id: '@pk'} , update: method: 'PUT')
]

app.factory 'Country', ['$resource', ($resource) ->
    $resource('/services/rest/country/:id', {id: '@pk'} , update: method: 'PUT')
]

app.factory 'User', ['$resource', ($resource) ->
    $resource '/services/rest/user/:id', id: '@id'
]

app.factory 'Position', ['$resource', ($resource) ->
    $resource('/services/rest/position/:id', {id: '@id'}, invalidate: {method: 'GET', url: '/services/rest/position/:id/invalidate'})
]

app.factory 'Split', ['$resource', ($resource) ->
    $resource '/services/rest/split/:id', id: '@id'
]

app.factory 'Operator', ['$resource', ($resource) ->
    $resource '/services/rest/operators/:id', id: '@id'
]

app.factory 'OptionPlan', ['$resource', ($resource) ->
    $resource '/services/rest/optionplan/:id', id: '@id'
]

app.factory 'OptionTransaction', ['$resource', ($resource) ->
    $resource '/services/rest/optiontransaction/:id', id: '@id'
]

app.factory 'Invitee', ['$resource', ($resource) ->
    $resource '/services/rest/invitee/:id', id: '@id'
]
