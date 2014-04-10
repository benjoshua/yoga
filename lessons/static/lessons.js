var lessonsApp = angular.module('LessonsApp', []);

lessonsApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

lessonsApp.controller('LessonsCtrl', ['$http', '$scope', function ($http, $scope) {

    $scope.lessons = [];

    $http.get('/lessons/rest_api/')
        .success(function (data) {
            $scope.lessons = data;
        });


}]);