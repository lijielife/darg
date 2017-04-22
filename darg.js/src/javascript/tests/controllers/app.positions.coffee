describe 'Unit: Testing Positions Controller', ->
  $controller = undefined
  $scope = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.positions')

  beforeEach inject(($rootScope, $controller) ->
    # The injector unwraps the underscores (_) from around the 
    # parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('PositionsController', $scope: $scope)
    return
  )

  describe 'add position', ->
    it 'resets all errors', ->
      $scope.errors = [{"field": "some error"}]
      $scope.add_position()
      expect($scope.errors).toEqual({})
