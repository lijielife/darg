describe 'Unit: Testing Start Controller', ->
  $controller = undefined
  $scope = undefined
  $httpBackend = undefined
  ctrl = undefined

  beforeEach module('js.darg.app.start')

  beforeEach inject(($rootScope, $controller, _$httpBackend_) ->
    # The injector unwraps the underscores (_) from around the parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('StartController', $scope: $scope)
    $httpBackend = _$httpBackend_
    return
  )

  beforeEach ->
      response = {results: []}
      $httpBackend.whenGET('/services/rest/shareholders').respond 200, response
      $httpBackend.whenGET('/services/rest/shareholders/option_holder').respond 200, response
      $httpBackend.whenGET('/services/rest/user').respond 200, {results: [{selected_company: '/company/23/'}]}
      $httpBackend.whenGET('/company/23/').respond 200, response
      $httpBackend.flush()

  describe 'method show_full_menu', ->
    it 'makes the hidden menu items visible', ->
      spyOn($scope, 'show_full_menu')
      $scope.show_full_menu()
      expect($scope.show_full_menu).toHaveBeenCalled()
      return
    return

  describe 'captable display', ->
    it 'should be displayed if there is one or less shareholders and a search', ->
        $scope.shareholders = [{name: 'shareholder1'}]
        $scope.search_params.query = 'test'
        $scope.$digest()
        expect($scope.hide_captable).toEqual false

    it 'should be hidden if there is one or less shareholders', ->
        $scope.shareholders = [{name: 'shareholder1'}]
        $scope.$digest()
        expect($scope.hide_captable).toEqual true

    it 'should be displayed if there are more than one shareholders', ->
        $scope.shareholders = [{name: 'shareholder1'}, {name: 'shareholder2'}]
        $scope.$digest()
        expect($scope.hide_captable).toEqual false

  describe 'method get new shareholder number', ->

    it 'returns a single number and updates the newShareholder obj.number', ->
      $httpBackend.expectGET('/services/rest/shareholders/get_new_shareholder_number').respond(
        200, {number: 790})
      $scope.get_new_shareholder_number()
      $httpBackend.flush()
      expect($scope.newShareholder.number).toEqual 790
