var lessonsApp = angular.module('LessonsApp', []);

lessonsApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

lessonsApp.controller('LessonsCtrl', ['$http', '$scope', function ($http, $scope) {

    $scope.lessons = [];

    $scope.getLessons = function () {
        $http.get('/lessons/rest_api/')
            .success(function (data) {
                $scope.lessons = data;
            });
    }

    $scope.getLessons();

    $scope.signup = function (lesson_id) {
        $http.post('/lessons/rest_api/signup/', {lesson: lesson_id})
            .success(function () {
                alert("signed up successfully");
                $scope.getLessons();
            })
            .error(function (data) {
                alert("error signing up: " + data);
            });

    }

    $scope.remove = function (lesson_id) {
        $http.post('/lessons/rest_api/remove/', {lesson: lesson_id})
            .success(function () {
                alert("removed successfully from class");
                $scope.getLessons();
            })
            .error(function (data) {
                alert("error removing: " + data);
            });

    }


}]);