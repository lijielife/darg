describe 'Unit: Testing Options Controller', ->
  $controller = undefined
  $scope = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.options')

  beforeEach inject(($rootScope, $controller) ->
    # The injector unwraps the underscores (_) from around the 
    # parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('OptionsController', $scope: $scope)
    return
  )

  describe 'method add_option_transaction', ->
    it 'resets errors', ->
      $scope.errors = [{"field": "some error"}]
      $scope.add_option_transaction()
      expect($scope.errors).toEqual({})
