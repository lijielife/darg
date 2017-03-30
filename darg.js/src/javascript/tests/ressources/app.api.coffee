describe 'Unit: Resource', ->

  beforeEach module('js.darg.api') 

  describe 'Postion api has invalidate method', ->

    it 'is defined', inject((Position) ->
      expect(Position).toBeDefined()
      return
    )


    it 'returns a resource function via invalidate method', inject((Position) ->
      output = Position
      expect(output).toEqual jasmine.any(Function)
      expect(output.invalidate({ id: 123 }.$promise)).toBeDefined()
      return
	)
