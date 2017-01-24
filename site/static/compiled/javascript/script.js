(function() {
  var app;

  app = angular.module('js.darg.api', ['ngResource']);

  app.factory('Shareholder', [
    '$resource', function($resource) {
      return $resource('/services/rest/shareholders/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('Security', [
    '$resource', function($resource) {
      return $resource('/services/rest/security/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('CompanyAdd', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/add/');
    }
  ]);

  app.factory('Company', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('Country', [
    '$resource', function($resource) {
      return $resource('/services/rest/country/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('User', [
    '$resource', function($resource) {
      return $resource('/services/rest/user/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Position', [
    '$resource', function($resource) {
      return $resource('/services/rest/position/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Split', [
    '$resource', function($resource) {
      return $resource('/services/rest/split/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Operator', [
    '$resource', function($resource) {
      return $resource('/services/rest/operators/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('OptionPlan', [
    '$resource', function($resource) {
      return $resource('/services/rest/optionplan/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('OptionTransaction', [
    '$resource', function($resource) {
      return $resource('/services/rest/optiontransaction/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Invitee', [
    '$resource', function($resource) {
      return $resource('/services/rest/invitee/:id', {
        id: '@id'
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.base', ['js.darg.api']);

  app.controller('BaseController', [
    '$scope', '$http', function($scope, $http) {
      return this.scope.test = True;
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.company', ['js.darg.api', 'xeditable', 'ngFileUpload', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('CompanyController', [
    '$scope', '$http', 'Company', 'Country', 'Operator', 'Upload', 'Security', '$timeout', function($scope, $http, Company, Country, Operator, Upload, Security, $timeout) {
      $scope.operators = [];
      $scope.company = null;
      $scope.errors = null;
      $scope.show_add_operator_form = false;
      $scope.file = null;
      $scope.logo_success = false;
      $scope.logo_errors = false;
      $scope.loading = false;
      $scope.newOperator = new Operator();
      $http.get('/services/rest/company/' + company_id).then(function(result) {
        $scope.company = new Company(result.data);
        $scope.company.founded_at = new Date($scope.company.founded_at);
        if ($scope.company.country) {
          return $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
        }
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      $http.get('/services/rest/operators').then(function(result) {
        return $scope.operators = result.data.results;
      });
      $scope.toggle_add_operator_form = function() {
        if ($scope.show_add_operator_form) {
          return $scope.show_add_operator_form = false;
        } else {
          return $scope.show_add_operator_form = true;
        }
      };
      $scope.delete_operator = function(pk) {
        return $http["delete"]('/services/rest/operators/' + pk).then(function() {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        });
      };
      $scope.add_operator = function() {
        $scope.newOperator.company = $scope.company.url;
        return $scope.newOperator.$save().then(function(result) {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        }).then(function() {
          return $scope.newOperator = new Operator();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.edit_security = function(security) {
        var sec;
        sec = new Security(security);
        return sec.$update().then(function(result) {
          var i;
          i = $scope.company.security_set.indexOf(security);
          return $scope.company.security_set[i] = result;
        }, function(rejection) {
          return rejection.data.number_segments[0];
        });
      };
      $scope.edit_company = function() {
        if ($scope.company.country) {
          $scope.company.country = $scope.company.country.url;
        }
        $scope.company.founded_at = $scope.company.founded_at.toISOString().substring(0, 10);
        return $scope.company.$update().then(function(result) {
          result.founded_at = new Date(result.founded_at);
          $scope.company = new Company(result);
          return $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.$watch('files', function() {
        $scope.upload($scope.files);
      });
      $scope.$watch('file', function() {
        if ($scope.file !== null) {
          $scope.files = [$scope.file];
        }
      });
      $scope.upload = function(files) {
        var file, i, payload;
        if (files && files.length) {
          $scope.loading = true;
          i = 0;
          while (i < files.length) {
            file = files[i];
            if (!file.$error) {
              payload = $scope.company;
              payload.founded_at = $scope.company.founded_at.toISOString().substring(0, 10);
              payload.logo = file;
              Upload.upload({
                url: '/services/rest/company/' + company_id + '/upload',
                data: payload,
                objectKey: '.k'
              }).then((function(response) {
                $timeout(function() {
                  var company;
                  company = new Company(response.data);
                  company.founded_at = new Date(company.founded_at);
                  $scope.company = company;
                  $scope.logo_success = true;
                  $scope.logo_errors = false;
                });
                return $timeout(function() {
                  $scope.logo_success = false;
                  return $scope.loading = false;
                }, 3000);
              }), (function(response) {
                return $timeout(function() {
                  $scope.logo_errors = response.data;
                  return $scope.loading = false;
                });
              }), function(evt) {
                Raven.captureException(evt, {
                  level: 'warning'
                });
              });
              return;
            }
          }
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd.MM.yy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.index', ['js.darg.api']);

  app.controller('IndexController', [
    '$scope', '$http', 'Invitee', function($scope, $http, Invitee) {
      $scope.show_add_invitee = true;
      $scope.newInvitee = new Invitee();
      $scope.errors = [];
      return $scope.add_invitee = function() {
        return $scope.newInvitee.$save().then(function(result) {
          $scope.show_add_invitee = false;
          if (!_.isUndefined(window.ga)) {
            return ga('send', 'event', 'click', 'save_invitee_email');
          }
        }).then(function() {
          return $scope.newInvitee = new Invitee();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.options', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionsController', [
    '$scope', '$http', '$window', '$filter', 'OptionPlan', 'OptionTransaction', function($scope, $http, $window, $filter, OptionPlan, OptionTransaction) {
      $scope.option_plans = [];
      $scope.optiontransactions = [];
      $scope.securities = [];
      $scope.loading = true;
      $scope.show_add_option_transaction = false;
      $scope.show_add_option_plan = false;
      $scope.show_optional_fields = false;
      $scope.newOptionPlan = new OptionPlan();
      $scope.newOptionPlan.board_approved_at = new Date();
      $scope.newOptionTransaction = new OptionTransaction();
      $scope.newOptionTransaction.bought_at = new Date();
      $scope.depot_types = [
        {
          name: gettext('Sperrdepot'),
          value: '2'
        }, {
          name: gettext('Zertifikatsdepot'),
          value: '0'
        }, {
          name: gettext('Gesellschaftsdepot'),
          value: '1'
        }
      ];
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = false;
      $scope.numberSegmentsAvailable = '';
      $scope.hasSecurityWithTrackNumbers = function() {
        var s;
        s = $scope.securities.find(function(el) {
          return el.track_numbers === true;
        });
        if (s !== void 0) {
          return true;
        }
      };
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        $scope.optiontransactions = [];
        return $scope.option_plans = [];
      };
      $scope.load_all = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        $http.get('/services/rest/optiontransaction').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.optiontransactions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        })["finally"](function() {
          return $scope.loading = false;
        });
        return $http.get('/services/rest/optionplan').then(function(result) {
          return angular.forEach(result.data.results, function(item) {
            return $scope.option_plans.push(item);
          });
        });
      };
      $scope.load_all();
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.optiontransactions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.optiontransactions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.search_shareholders = function(term) {
        var paramss;
        paramss = {
          search: term
        };
        return $http.get('/services/rest/shareholders', {
          params: paramss
        }).then(function(response) {
          return response.data.results.map(function(item) {
            return item;
          });
        });
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        console.log(params);
        return $http.get('/services/rest/optiontransaction?' + paramss).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.optiontransactions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.query;
        });
      };
      $scope.add_option_plan = function() {
        var date;
        if ($scope.newOptionPlan.board_approved_at) {
          date = $scope.newOptionPlan.board_approved_at;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.newOptionPlan.board_approved_at = date.toISOString().substring(0, 10);
        }
        return $scope.newOptionPlan.$save().then(function(result) {
          return $scope.load_all();
        }).then(function() {
          $scope.newOptionPlan = new OptionPlan();
          return $scope.show_add_option_plan = false;
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-optionplan');
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          if (date) {
            return $scope.newOptionPlan.board_approved_at = date;
          }
        });
      };
      $scope.add_option_transaction = function() {
        var date, p;
        if ($scope.newOptionTransaction.option_plan) {
          p = $scope.newOptionTransaction.option_plan;
        }
        if ($scope.newOptionTransaction.bought_at) {
          date = $scope.newOptionTransaction.bought_at;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.newOptionTransaction.bought_at = date.toISOString().substring(0, 10);
        }
        if ($scope.newOptionTransaction.depot_type) {
          $scope.newOptionTransaction.depot_type = $scope.newOptionTransaction.depot_type.value;
        }
        return $scope.newOptionTransaction.$save().then(function(result) {
          return $scope.load_all();
        }).then(function() {
          $scope.newOptionTransaction = new OptionTransaction();
          return $scope.show_add_option_transaction = false;
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-option-transaction');
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          $scope.newOptionTransaction.bought_at = date;
          return $scope.newOptionTransaction.option_plan = p;
        });
      };
      $scope.delete_option_transaction = function(option_transaction) {
        return $http["delete"]('/services/rest/optiontransaction/' + option_transaction.pk).then(function(result) {
          return $scope.load_all();
        });
      };
      $scope.confirm_option_transaction = function(option_transaction) {
        return $http.post('/services/rest/optiontransaction/' + option_transaction.pk + '/confirm').then(function(result) {
          return $scope.load_all();
        });
      };
      $scope.show_add_option_plan_form = function() {
        $scope.show_add_option_plan = true;
        $scope.show_add_option_transaction = false;
        return $scope.newOptionPlan = new OptionPlan();
      };
      $scope.show_add_option_transaction_form = function() {
        $scope.show_add_option_transaction = true;
        $scope.show_add_option_plan = false;
        return $scope.newOptionTransaction = new OptionTransaction();
      };
      $scope.hide_form = function() {
        $scope.show_add_option_plan = false;
        $scope.show_add_option_transaction = false;
        $scope.newOptionPlan = new OptionPlan();
        return $scope.newOptionTransaction = new OptionTransaction();
      };
      $scope.show_available_number_segments_for_new_option_plan = function() {
        var url;
        if ($scope.newOptionPlan.security) {
          if ($scope.newOptionPlan.security.track_numbers) {
            url = '/services/rest/shareholders/company_number_segments';
            if ($scope.newOptionPlan.board_approved_at) {
              url = url + '?date=' + $scope.newOptionPlan.board_approved_at.toISOString();
            }
            return $http.get(url).then(function(result) {
              if ($scope.newOptionPlan.security.pk in result.data && result.data[$scope.newOptionPlan.security.pk].length > 0) {
                return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data[$scope.newOptionPlan.security.pk];
              } else {
                return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: None');
              }
            });
          } else {
            return $scope.numberSegmentsAvailable = '';
          }
        }
      };
      $scope.show_available_number_segments_for_new_option_transaction = function() {
        var op_pk, sh_pk, url;
        if ($scope.newOptionTransaction.seller && $scope.newOptionTransaction.option_plan && $scope.newOptionTransaction.option_plan.security.track_numbers) {
          op_pk = $scope.newOptionTransaction.option_plan.pk.toString();
          sh_pk = $scope.newOptionTransaction.seller.pk.toString();
          url = '/services/rest/optionplan/' + op_pk + '/number_segments/' + sh_pk;
          if ($scope.newOptionTransaction.bought_at) {
            url = url + '?date=' + $scope.newOptionTransaction.bought_at.toISOString();
          }
          return $http.get(url).then(function(result) {
            if (result.data && result.data.length > 0) {
              return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data;
            } else {
              return $scope.numberSegmentsAvailable = gettext('No security segments available for option plan on selected date or now.');
            }
          });
        }
      };
      $scope.toggle_optional_fields = function() {
        if ($scope.show_optional_fields) {
          return $scope.show_optional_fields = false;
        } else {
          return $scope.show_optional_fields = true;
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
      return $scope.goto_option = function(option_id) {
        return window.location = "/options/" + option_id + "/";
      };
    }
  ]);

  app.directive('stringToNumber', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        ngModel.$parsers.push(function(value) {
          return '' + value;
        });
        ngModel.$formatters.push(function(value) {
          return parseFloat(value);
        });
      }
    };
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.optionplan', ['js.darg.api', 'xeditable', 'ngFileUpload', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionPlanController', [
    '$scope', '$http', 'OptionPlan', 'Upload', '$timeout', function($scope, $http, OptionPlan, Upload, $timeout) {
      $scope.file = null;
      $scope.pdf_upload_success = false;
      $scope.pdf_upload_errors = false;
      $scope.loading = false;
      $http.get('/services/rest/optionplan/' + optionplan_id).then(function(result) {
        $scope.optionplan = new OptionPlan(result.data);
        return $scope.optionplan.board_approved_at = $scope.optionplan.board_approved_at;
      });
      $http.get('/services/rest/security').then(function(result) {
        return $scope.securities = result.data.results;
      });
      $scope.$watch('files', function() {
        $scope.upload($scope.files);
      });
      $scope.$watch('file', function() {
        if ($scope.file !== null) {
          $scope.files = [$scope.file];
        }
      });
      return $scope.upload = function(files) {
        var file, i, payload;
        if (files && files.length) {
          $scope.loading = true;
          i = 0;
          while (i < files.length) {
            file = files[i];
            if (!file.$error) {
              payload = $scope.optionplan;
              payload.pdf_file = file;
              Upload.upload({
                url: '/services/rest/optionplan/' + optionplan_id + '/upload',
                data: payload,
                objectKey: '.k'
              }).then((function(response) {
                $timeout(function() {
                  $scope.optionplan = response.data;
                  $scope.pdf_upload_success = true;
                  $scope.pdf_upload_errors = false;
                });
                return $timeout(function() {
                  $scope.pdf_upload_success = false;
                  return $scope.loading = false;
                }, 3000);
              }), (function(response) {
                return $timeout(function() {
                  $scope.pdf_upload_errors = response.data;
                  return $scope.loading = false;
                });
              }), function(evt) {
                Raven.captureException(evt, {
                  level: 'warning'
                });
              });
              return;
            }
          }
        }
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.optiontransaction', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionTransactionController', [
    '$scope', '$http', 'OptionTransaction', function($scope, $http, OptionTransaction) {
      $scope.optiontransaction = true;
      return $http.get('/services/rest/optiontransaction/' + optiontransaction_id).then(function(result) {
        return $scope.optiontransaction = new OptionTransaction(result.data);
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.positions', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('PositionsController', [
    '$scope', '$http', '$window', 'Position', 'Split', function($scope, $http, $window, Position, Split) {
      $scope.positions = [];
      $scope.securities = [];
      $scope.show_add_position = false;
      $scope.show_add_capital = false;
      $scope.show_split_data = false;
      $scope.show_split = false;
      $scope.show_optional_fields = false;
      $scope.newPosition = new Position();
      $scope.newSplit = new Split();
      $scope.depot_types = [
        {
          name: gettext('Sperrdepot'),
          value: '2'
        }, {
          name: gettext('Zertifikatsdepot'),
          value: '0'
        }, {
          name: gettext('Gesellschaftsdepot'),
          value: '1'
        }
      ];
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = false;
      $scope.numberSegmentsAvailable = '';
      $scope.hasSecurityWithTrackNumbers = function() {
        var s;
        s = $scope.securities.find(function(el) {
          return el.track_numbers === true;
        });
        if (s !== void 0) {
          return true;
        }
      };
      $scope.positionsLoading = true;
      $scope.addPositionLoading = false;
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        return $scope.positions = [];
      };
      $scope.load_all_positions = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        return $http.get('/services/rest/position').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.positions.push(item);
          });
          $scope.positionsLoading = false;
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        });
      };
      $scope.load_all_positions();
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.positions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.positions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.search_shareholders = function(term) {
        var paramss;
        paramss = {
          search: term
        };
        return $http.get('/services/rest/shareholders', {
          params: paramss
        }).then(function(response) {
          return response.data.results.map(function(item) {
            return item;
          });
        });
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/position', {
          params: params
        }).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.positions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.search;
        });
      };
      $scope.add_position = function() {
        var bought_at;
        $scope.addPositionLoading = true;
        if ($scope.newPosition.bought_at) {
          bought_at = $scope.newPosition.bought_at;
          bought_at.setHours(bought_at.getHours() - bought_at.getTimezoneOffset() / 60);
          $scope.newPosition.bought_at = bought_at;
        }
        if ($scope.newPosition.depot_type) {
          $scope.newPosition.depot_type = $scope.newPosition.depot_type.value;
        }
        return $scope.newPosition.$save().then(function(result) {
          return $scope.positions.push(result);
        }).then(function() {
          $scope.show_add_position = false;
          $scope.show_add_capital = false;
          return $scope.newPosition = new Position();
        }).then(function() {
          $scope.errors = null;
          $window.ga('send', 'event', 'form-send', 'add-transaction');
          return $scope.addPositionLoading = false;
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          return $scope.addPositionLoading = false;
        });
      };
      $scope.delete_position = function(position) {
        $scope.positionsLoading = true;
        return $http["delete"]('/services/rest/position/' + position.pk).then(function(result) {
          $scope.positions = [];
          $http.get('/services/rest/position').then(function(result1) {
            return angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
          });
          return $scope.positionsLoading = false;
        });
      };
      $scope.confirm_position = function(position) {
        return $http.post('/services/rest/position/' + position.pk + '/confirm').then(function(result) {
          $scope.positions = [];
          return $http.get('/services/rest/position').then(function(result1) {
            angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
            return $scope.positionsLoading = false;
          });
        });
      };
      $scope.add_split = function() {
        var execute_at;
        execute_at = $scope.newSplit.execute_at;
        execute_at.setHours(execute_at.getHours() - execute_at.getTimezoneOffset() / 60);
        $scope.newSplit.execute_at = execute_at;
        return $scope.newSplit.$save().then(function(result) {
          return $scope.positions = result.data;
        }).then(function() {
          return $scope.newSplit = new Split();
        }).then(function() {
          $scope.errors = null;
          $scope.show_split = false;
          return $window.ga('send', 'event', 'form-send', 'add-split');
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.show_add_position_form = function() {
        $scope.show_add_position = true;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.toggle_show_split_data = function() {
        if ($scope.show_split_data) {
          return $scope.show_split_data = false;
        } else {
          return $scope.show_split_data = true;
        }
      };
      $scope.toggle_optional_fields = function() {
        if ($scope.show_optional_fields) {
          return $scope.show_optional_fields = false;
        } else {
          return $scope.show_optional_fields = true;
        }
      };
      $scope.show_add_capital_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = true;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.hide_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.show_split_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newSplit = new Split();
        return $scope.show_split = true;
      };
      $scope.show_available_number_segments = function() {
        var url;
        if ($scope.newPosition.security) {
          if ($scope.newPosition.security.track_numbers && $scope.newPosition.seller) {
            url = '/services/rest/shareholders/' + $scope.newPosition.seller.pk.toString() + '/number_segments';
            if ($scope.newPosition.bought_at) {
              url = url + '?date=' + $scope.newPosition.bought_at.toISOString();
            }
            return $http.get(url).then(function(result) {
              if ($scope.newPosition.security.pk in result.data && result.data[$scope.newPosition.security.pk].length > 0) {
                return $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: ') + result.data[$scope.newPosition.security.pk];
              } else {
                return $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: None');
              }
            });
          }
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
      return $scope.goto_position = function(position_id) {
        return window.location = "/positions/" + position_id + "/";
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.position', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('PositionController', [
    '$scope', '$http', 'Position', function($scope, $http, Position) {
      $scope.position = true;
      $scope.errors = null;
      return $http.get('/services/rest/position/' + position_id).then(function(result) {
        return $scope.position = new Position(result.data);
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.reports', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('ReportsController', ['$scope', '$http', 'Shareholder', function($scope, $http, Shareholder) {}]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.shareholder', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('ShareholderController', [
    '$scope', '$http', 'Shareholder', function($scope, $http, Shareholder) {
      $scope.shareholder = true;
      $scope.countries = [];
      $scope.languages = [];
      $scope.errors = null;
      $scope.legal_types = [
        {
          name: gettext('Human Being'),
          value: 'H'
        }, {
          name: gettext('Corporate'),
          value: 'C'
        }
      ];
      $scope.mailing_types = [
        {
          name: gettext('Not deliverable'),
          value: '0'
        }, {
          name: gettext('Postal Mail'),
          value: '1'
        }, {
          name: gettext('via Email'),
          value: '2'
        }
      ];
      $http.get('/services/rest/shareholders/' + shareholder_id).then(function(result) {
        var legal_type, mailing_type;
        if (result.data.user.userprofile.birthday !== null) {
          result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday);
        }
        $scope.shareholder = new Shareholder(result.data);
        if ($scope.shareholder.user.userprofile.country) {
          $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
            return $scope.shareholder.user.userprofile.country = result1.data;
          });
        }
        if ($scope.shareholder.user.userprofile.nationality) {
          $http.get($scope.shareholder.user.userprofile.nationality).then(function(result1) {
            return $scope.shareholder.user.userprofile.nationality = result1.data;
          });
        }
        legal_type = $scope.legal_types.filter(function(obj) {
          return obj.value === $scope.shareholder.user.userprofile.legal_type;
        });
        $scope.shareholder.user.userprofile.legal_type = legal_type[0];
        mailing_type = $scope.mailing_types.filter(function(obj) {
          return obj.value === $scope.shareholder.mailing_type;
        });
        return $scope.shareholder.mailing_type = mailing_type[0];
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      $http.get('/services/rest/language').then(function(result) {
        return $scope.languages = result.data;
      });
      $scope.edit_shareholder = function() {
        var date;
        if ($scope.shareholder.user.userprofile.birthday) {
          date = $scope.shareholder.user.userprofile.birthday;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.shareholder.user.userprofile.birthday = date;
        }
        if ($scope.shareholder.user.userprofile.country) {
          $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url;
        }
        if ($scope.shareholder.user.userprofile.nationality) {
          $scope.shareholder.user.userprofile.nationality = $scope.shareholder.user.userprofile.nationality.url;
        }
        if ($scope.shareholder.user.userprofile.language) {
          $scope.shareholder.user.userprofile.language = $scope.shareholder.user.userprofile.language.iso;
        }
        if ($scope.shareholder.user.userprofile.legal_type) {
          $scope.shareholder.user.userprofile.legal_type = $scope.shareholder.user.userprofile.legal_type.value;
        }
        if ($scope.shareholder.mailing_type) {
          $scope.shareholder.mailing_type = $scope.shareholder.mailing_type.value;
        }
        return $scope.shareholder.$update().then(function(result) {
          if (result.user.userprofile.birthday !== null) {
            result.user.userprofile.birthday = new Date(result.user.userprofile.birthday);
          }
          $scope.shareholder = new Shareholder(result);
          if ($scope.shareholder.user.userprofile.country) {
            $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
              return $scope.shareholder.user.userprofile.country = result1.data;
            });
          }
          if ($scope.shareholder.user.userprofile.nationality) {
            return $http.get($scope.shareholder.user.userprofile.nationality).then(function(result1) {
              return $scope.shareholder.user.userprofile.nationality = result1.data;
            });
          }
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd.MM.yy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
    }
  ]);

  app.filter('percentage', [
    '$filter', function($filter) {
      return function(input, decimals) {
        return $filter('number')(input * 100, decimals) + '%';
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.start', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('StartController', [
    '$scope', '$window', '$http', 'CompanyAdd', 'Shareholder', 'User', 'Company', '$timeout', function($scope, $window, $http, CompanyAdd, Shareholder, User, Company, $timeout) {
      $scope.shareholders = [];
      $scope.option_holders = [];
      $scope.user = [];
      $scope.total_shares = 0;
      $scope.loading = true;
      $scope.shareholder_added_success = false;
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = [
        {
          'name': gettext('Email'),
          'value': 'user__email'
        }, {
          'name': gettext('Shareholder Number'),
          'value': 'number'
        }, {
          'name': gettext('Last Name'),
          'value': 'user__last_name'
        }
      ];
      $scope.optionholder_next = false;
      $scope.optionholder_previous = false;
      $scope.optionholder_total = 0;
      $scope.optionholder_current = 0;
      $scope.optionholder_current_range = '';
      $scope.optionholder_search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.optionholder_ordering_options = [
        {
          'name': gettext('Email'),
          'value': 'user__email'
        }, {
          'name': gettext('Shareholder Number'),
          'value': 'number'
        }, {
          'name': gettext('Last Name'),
          'value': 'user__last_name'
        }
      ];
      $scope.show_add_shareholder = false;
      $scope.newShareholder = new Shareholder();
      $scope.newCompany = new CompanyAdd();
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        return $scope.shareholders = [];
      };
      $scope.optionholder_reset_search_params = function() {
        $scope.optionholder_current = null;
        $scope.optionholder_previous = null;
        $scope.optionholder_next = null;
        return $scope.option_holders = [];
      };
      $scope.load_option_holders = function(company_pk) {
        return $http.get('/services/rest/shareholders/option_holder?company=' + company_pk).then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.option_holders.push(item);
          });
          if (result.data.next) {
            $scope.optionholder_next = result.data.next;
          }
          if (result.data.previous) {
            $scope.optionholder_previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.optionholder_total = result.data.count;
          }
          if (result.data.current) {
            return $scope.optionholder_current = result.data.current;
          }
        });
      };
      $scope.load_all_shareholders = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        return $http.get('/services/rest/shareholders').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.shareholders.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        });
      };
      $scope.load_all_shareholders();
      $http.get('/services/rest/user').then(function(result) {
        $scope.user = result.data.results[0];
        angular.forEach($scope.user.operator_set, function(item, key) {
          return $http.get(item.company).then(function(result1) {
            $scope.user.operator_set[key].company = result1.data;
            return $scope.load_option_holders(result1.data.pk);
          });
        });
        if ($scope.user.operator_set && $scope.user.operator_set[0].company.pk) {
          return $scope.load_option_holders($scope.user.operator_set[0].company.pk);
        }
      })["finally"](function() {
        return $scope.loading = false;
      });
      $scope.$watchCollection('shareholders', function(shareholders) {
        $scope.total_shares = 0;
        return angular.forEach(shareholders, function(item) {
          return $scope.total_shares = item.share_count + $scope.total_shares;
        });
      });
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.$watchCollection('optionholder_current', function(optionholder_current) {
        var end, start;
        start = ($scope.optionholder_current - 1) * 20;
        end = Math.min($scope.optionholder_current * 20, $scope.optionholder_total);
        return $scope.optionholder_current_range = start.toString() + '-' + end.toString();
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.shareholders.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.shareholders.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.optionholder_next_page = function() {
        if ($scope.optionholder_next) {
          return $http.get($scope.optionholder_next).then(function(result) {
            $scope.optionholder_reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.option_holders.push(item);
            });
            if (result.data.next) {
              $scope.optionholder_next = result.data.next;
            } else {
              $scope.optionholder_next = false;
            }
            if (result.data.previous) {
              $scope.optionholder_previous = result.data.previous;
            } else {
              $scope.optionholder_previous = false;
            }
            if (result.data.count) {
              $scope.optionholder_total = result.data.count;
            }
            if (result.data.current) {
              return $scope.optionholder_current = result.data.current;
            }
          });
        }
      };
      $scope.optionholder_previous_page = function() {
        if ($scope.optionholder_previous) {
          return $http.get($scope.optionholder_previous).then(function(result) {
            $scope.optionholder_reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.option_holders.push(item);
            });
            if (result.data.next) {
              $scope.optionholder_next = result.data.next;
            } else {
              $scope.optionholder_next = false;
            }
            if (result.data.previous) {
              $scope.optionholder_previous = result.data.previous;
            } else {
              $scope.optionholder_previous = false;
            }
            if (result.data.count) {
              $scope.optionholder_total = result.data.count;
            }
            if (result.data.current) {
              return $scope.optionholder_current = result.data.current;
            }
          });
        }
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/shareholders?' + paramss).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.shareholders.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.search;
        });
      };
      $scope.optionholder_search = function() {
        var params, paramss;
        params = {};
        params.company = $scope.user.operator_set[0].company.pk;
        if ($scope.optionholder_search_params.query) {
          params.search = $scope.optionholder_search_params.query;
        }
        if ($scope.optionholder_search_params.ordering) {
          params.ordering = $scope.optionholder_search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/shareholders/option_holder?' + paramss).then(function(result) {
          $scope.optionholder_reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.option_holders.push(item);
          });
          if (result.data.next) {
            $scope.optionholder_next = result.data.next;
          }
          if (result.data.previous) {
            $scope.optionholder_previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.optionholder_total = result.data.count;
          }
          if (result.data.current) {
            $scope.optionholder_current = result.data.current;
          }
          return $scope.optionholder_search_params.query = params.search;
        });
      };
      $scope.add_company = function() {
        return $scope.newCompany.$save().then(function(result) {
          return $http.get('/services/rest/user').then(function(result) {
            $scope.user = result.data.results[0];
            return angular.forEach($scope.user.operator_set, function(item, key) {
              return $http.get(item.company).then(function(result1) {
                return $scope.user.operator_set[key].company = result1.data;
              });
            });
          }).then(function() {
            return $scope.load_all_shareholders();
          });
        }).then(function() {
          $scope.company = new Company();
          return $window.ga('send', 'event', 'form-send', 'add-company');
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.add_shareholder = function() {
        return $scope.newShareholder.$save().then(function(result) {
          return $scope.shareholders.push(result);
        }).then(function() {
          $scope.newShareholder = new Shareholder();
          $scope.shareholder_added_success = true;
          return $timeout(function() {
            return $scope.shareholder_added_success = false;
          }, 30000);
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-shareholder');
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.show_add_shareholder_form = function() {
        return $scope.show_add_shareholder = true;
      };
      $scope.hide_form = function() {
        return $scope.show_add_shareholder = false;
      };
      $scope.goto_shareholder = function(shareholder_id) {
        return window.location = "/shareholder/" + shareholder_id + "/";
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.tfa', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('TwoFactorAuthenticationController', [
    '$scope', '$http', '$window', '$filter', function($scope, $http, $window, $filter) {
      return $scope.submit = function() {
        $('form')[0].submit();
        return console.log('f');
      };
    }
  ]);

}).call(this);

(function() {
  $('.table tr').each(function() {
    $(this).css('cursor', 'pointer').hover((function() {
      $(this).addClass('active');
    }), function() {
      $(this).removeClass('active');
    });
  });

  return;

}).call(this);
