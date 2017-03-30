describe 'Unit: Testing Start Controller', ->
  $controller = undefined
  $scope = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.start') 

  beforeEach inject(($rootScope, $controller) ->
    # The injector unwraps the underscores (_) from around the parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('StartController', $scope: $scope)
    return
  )

  describe '$scope.user', ->
    it 'sets the strength to "strong" ', ->
      $scope.strength = 'strong'
      expect($scope.strength).toEqual 'strong'
      return
    return
