angular
    .module('AvalApp', ['ngRoute'])
    .config(aval_config)
    .controller('LoginCtrl', LoginCtrl)
    .controller('QuestController', QuestController)

var url = '/aval/'

function LoginCtrl( $scope, $http, $location ) {
    $scope.login = {};
    $scope.enablebtn = true;
    
    $scope.senddata = function(){
        $scope.login.page = 'login'
        $http.post(url, $scope.login)
            .then(function(response){
                if (response.data.status == 'ok'){
                    $location.path('/questionario/')
                }else{
                    console.log(response.data.msg)
                }   
            }
        );
    }
}
LoginCtrl.$inject = ['$scope', '$http', '$location'];

function QuestController($scope, $http, $location){
    console.log('questionários baby...')
}
QuestController.$inject = ['$scope', '$http', '$location'];

function aval_config( $routeProvider ) {
    var pfx = '/static/templates/';

    $routeProvider
        .when( '/',                            { templateUrl: pfx + 'main.html'            })
        .when( '/questionario/',         { templateUrl: pfx + 'quest.html'         })
        .otherwise({redirectTo: '/' })
        ;
}
aval_config.$inject = [ '$routeProvider' ];

// angular.module('avalApp', [])
//     .controller('MainController', function($http) {
//     var mainCtlr = this;
//     var url = '/candidate/'
//     var candidate_id = null

//     mainCtlr.magic = function(){
//         alert('nice')
//         console.log('nice')
//     };

//     mainCtlr.senddata = function(){
//         //TODO - criar validação dos campos de nome e email
//         var post_data = {}
//         post_data.page = 'login'
//         post_data.name = mainCtlr.name;
//         post_data.email = mainCtlr.email;
//         $http.post(url, post_data).then(function(response){
//                 var data = response.data
//                 if (response.status == 200 && data.status == 'ok') {
//                     $http.get(url+'?page=questionario')
//                 }
//             });
//     };

// });
