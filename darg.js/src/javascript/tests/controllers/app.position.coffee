describe 'Unit: Testing Position Controller', ->
  $controller = undefined
  $scope = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.position') 

  beforeEach inject(($rootScope, $controller) ->
    # The injector unwraps the underscores (_) from around the parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('PositionController', $scope: $scope)
    return
  )

  describe 'methods', ->
    it 'should have certificate invalidation method', ->
      # expect($scope.invalidate_certificate).toEqual jasmine.any(Function)
      return
    return
  
