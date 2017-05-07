describe 'Unit: Testing Reports Controller', ->
  $controller = undefined
  $scope = undefined
  $httpBackend = undefined
  $response = {results: [{report_type: 'captableX', order_by: 'share_count', file_type: 'PDF', report_at: new Date()}]}
  ctrl = undefined

  beforeEach module('js.darg.app.reports') 

  beforeEach inject(($rootScope, $controller, _$httpBackend_) ->
    # The injector unwraps the underscores (_) from around the parameter names
    $scope = $rootScope.$new()
    ctrl = $controller('ReportsController', $scope: $scope)
    $httpBackend = _$httpBackend_
    return
  )

  beforeEach ->
      $httpBackend.whenGET('/services/rest/security').respond 200, {}
      $httpBackend.whenGET(/\/services\/rest\/report?.*/g).respond 200, $response
      $httpBackend.flush()

  describe 'helper methods specs:', ->
    it 'should convert string to ordering obj', ->
      expect($scope.lookup_ordering('share_count').value).toEqual 'share_count'
 
    it 'should replace ordering inside json response by obj', ->
      expect($scope.get_report_from_api_result(
        {data: results: [{order_by: 'share_count'}]}).order_by.value 
      ).toEqual 'share_count'

  describe 'get_captable_report methods specs:', ->

    it 'should set default report obj when server sends empty response', ->
      $scope.last_captable_report.report_type = 'captable'
      $httpBackend.expectGET(/\/services\/rest\/report?.*/g).respond 200, {results: []}
      $scope.get_captable_report()
      $httpBackend.flush()
      expect($scope.last_captable_report.report_type).toEqual 'captable'

    it 'should send a proper http query to fetch last captable report', ->
      $httpBackend.expectGET(/\/services\/rest\/report?.*/g).respond 200, $response
      $scope.get_captable_report()
      $httpBackend.flush()
      expect($scope.last_captable_report.report_type).toEqual $response.results[0].report_type

  describe 'get_all_securities helper methods specs:', ->

    it 'should get all securities for company', ->
      $httpBackend.expectGET('/services/rest/security').respond(
        200, {results: [{pk: '1'}]})
      $scope.get_all_securities()
      $httpBackend.flush()
      expect($scope.securities.length).toEqual 1

  describe 'add_captable_report should POST proper request', ->
    it 'should put the response inside last_captable_report', ->
      $httpBackend.expectPOST('/services/rest/report').respond(
        201, {report_type: 'captableZ', order_by: 'share_percent', 
        report_at: new Date()})
      $scope.add_captable_report()
      $httpBackend.flush()
      expect($scope.last_captable_report.report_type).toEqual 'captableZ'
      expect($scope.last_captable_report.order_by.value).toEqual 'share_percent'

  describe 'ordering options', ->
    it 'should have 14 options', ->
      expect($scope.captable_orderings.length).toEqual 14
