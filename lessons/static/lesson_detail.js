var lessonDetail = angular.module('LessonDetail', []);

lessonDetail.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

lessonDetail.controller('LessonDetailCtrl', ['$http', '$scope', function ($http, $scope) {

    $scope.lesson = [];

    $scope.getLesson = function (lesson_id) {
        $http.get('/lessons/rest_api/' + lesson_id)
            .success(function (data) {
                $scope.lesson = data;
            });
    }

    $scope.getLesson(1);

}]);