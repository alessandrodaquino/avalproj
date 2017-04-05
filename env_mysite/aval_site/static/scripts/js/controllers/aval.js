angular
    .module('AvalApp', ['ngRoute'])
    .config(aval_config)
    .controller('LoginCtrl', LoginCtrl)
    .controller('QuestController', QuestController)

var url = '/aval/'

function LoginCtrl( $scope, $http, $location ) {
    $scope.login = {};
    $scope.enablebtn = true;
    $scope.valid_input = {}
    $scope.valid_input.name = true; //Input for name is valid or not
    $scope.valid_input.email = true;
    $scope.err_msg = ''

    $scope.senddata = function(){
        $scope.login.page = 'login'
        $http.post(url, $scope.login)
            .then(function(response){
                if (response.data.status == 'ok'){
                    console.log(response.data)
                    $location.path('/questionario/'+ response.data.idcandidate)
                }else{
                    console.log(response.data)
                    $scope.err_msg = response.data.msg;
                    $scope.valid_input.name = response.data.fname;
                    $scope.valid_input.femail = response.data.femail;
                }   
            }
        );
    }
}
LoginCtrl.$inject = ['$scope', '$http', '$location'];

function QuestController($scope, $http, $location, $routeParams){
    $scope.answer = {};
    $scope.qtn_list = [];
    var idcandidate = $routeParams.idcandidate;

    $scope.opts = [
        {'val': 0, 'desc': 0},
        {'val': 1, 'desc': 1},
        {'val': 2, 'desc': 2},
        {'val': 3, 'desc': 3},
        {'val': 4, 'desc': 4},
        {'val': 5, 'desc': 5},
        {'val': 6, 'desc': 6},
        {'val': 7, 'desc': 7},
        {'val': 8, 'desc': 8},
        {'val': 9, 'desc': 9},
        {'val': 10, 'desc': 10},
    ]

    $scope.senddata = function(){
        $scope.answer.page = 'quest'
        $scope.answer.answers = $scope.qtn_list
        $scope.answer.idcandidate = idcandidate
        $http.post(url, $scope.answer)
            .then(function(response){
                console.log(response.data)
                if (response.data.status == 'ok'){
                    
                }
            });
    };

    $scope.onload = function(){
        console.log(idcandidate)
        $http.get(url + '?page=quest&idcandidate='+idcandidate)
            .then(function(response){
                if (response.data.status == 'ok'){
                    $scope.qtn_list = JSON.parse(response.data.questions)
                }else if(response.data.status == 'completed' || response.data.status == 'not_found'){
                    alert(response.data.msg)//sim, não é elegante, é horrivel usar isso
                    $location.path('/')
                }
            }
        );
    };

    $scope.onload()


}
QuestController.$inject = ['$scope', '$http', '$location', '$routeParams'];

function aval_config( $routeProvider ) {
    var pfx = '/static/templates/';

    $routeProvider
        .when( '/', { templateUrl: pfx + 'main.html'})
        .when( '/questionario/:idcandidate', { templateUrl: pfx + 'quest.html'})
        .otherwise({redirectTo: '/' })
        ;
}
aval_config.$inject = [ '$routeProvider' ];
