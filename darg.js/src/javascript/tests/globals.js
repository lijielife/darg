// required to run tests is the faking of the django 
// translation mechanism
var gettext = function() {
  return
}

var django = {'catalog': {}}

// custom defined vars
position_id = 1
