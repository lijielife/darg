describe 'Unit: Testing Start Controller', ->
  $controller = undefined
  $scope = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.start')

  beforeEach inject(($rootScope, $controller) ->
    # The injector unwraps the underscores (_) from around the 
    # parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('StartController', $scope: $scope)
    return
  )

  describe 'method show_full_menu', ->
    it 'makes the hidden menu items visible', ->
      spyOn($scope, 'show_full_menu')
      $scope.show_full_menu()
      expect($scope.show_full_menu).toHaveBeenCalled()
      return
    return
