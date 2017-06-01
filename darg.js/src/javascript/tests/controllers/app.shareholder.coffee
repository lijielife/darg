describe 'Unit: Testing Shareholder Detail Controller', ->
  $controller = undefined
  $scope = undefined
  $httpBackend = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.shareholder')

  beforeEach inject(($rootScope, $controller, _$httpBackend_) ->
    # The injector unwraps the underscores (_) from around the parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('ShareholderController', $scope: $scope)
    $httpBackend = _$httpBackend_
    return
  )

  # beforeEach ->
      # response = {results: []}
      # $httpBackend.whenGET('/services/rest/shareholders').respond 200, response
      # $httpBackend.whenGET('/services/rest/shareholders/option_holder').respond 200, response
      # $httpBackend.whenGET('/services/rest/user').respond 200, {results: [{selected_company: '/company/23/'}]}
      # $httpBackend.whenGET('/company/23/').respond 200, response
      # $httpBackend.flush()

  describe 'method toggle_locked_positions', ->
    it 'shows or hides locked positions', ->
      $scope.toggle_locked_positions(1)
      expect($scope.locked_positions_security).toEqual 1
    it 'closes other opened locked position elements', ->
        $scope.locked_positions_security = 1
        $scope.toggle_locked_positions(2)
        expect($scope.locked_positions_security).toEqual 2
    it 'closes on the second trigger', ->
        $scope.locked_positions_security = 1
        $scope.toggle_locked_positions(1)
        expect($scope.locked_positions_security).toEqual null
