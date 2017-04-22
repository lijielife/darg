var main = require('./karma.conf.js');

module.exports = function(config) {

  main(config);

  config.set({


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true,

  })
}
