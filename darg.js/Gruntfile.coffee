module.exports = (grunt) ->

    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        watch:
            coffee:
                files: ['src/javascript/app.*.coffee']
                tasks: ['coffee', 'concat:dist', 'copy']
        coffee:
            files:
                # add deps here
                src: [
                    'src/javascript/app.*.coffee',
                ]
                dest: 'compiled/javascript/application.js'

        copy:
            main:
                expand: true
                src: 'compiled/javascript/script.js'
                dest: '../site/static/'

        concat:
            dist:
                options: separator: ';'
                src: [
                  './darg.js/assets/jquery/dist/jquery.js',
                  './darg.js/assets/raven-js/dist/raven.js',
                  './darg.js/assets/underscore/underscore.js',
                  './darg.js/assets/angular/angular.min.js',
                  './darg.js/assets/angular-mocks/angular-mocks.js',
                  './darg.js/assets/angular-animate/angular-animate.js',
                  './darg.js/assets/angular-bootstrap/ui-bootstrap-tpls.js',
                  './darg.js/assets/angular-resource/angular-resource.js',
                  './darg.js/assets/angular-translate/angular-translate.js',
                  './darg.js/assets/bootstrap/dist/js/bootstrap.min.js',
                  './darg.js/assets/angular-xeditable/dist/js/xeditable.js',
                  './darg.js/assets/ng-file-upload/ng-file-upload.js',
                  './darg.js/assets/angular-i18n/angular-locale_de-ch.js',
                  'compiled/javascript/application.js'
                ]
                dest: 'compiled/javascript/script.js'

    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-contrib-copy')
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.registerTask('default', ['coffee'], 'watch')
    grunt.registerTask('default', ['copy'], 'watch')
