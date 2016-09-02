(function(window, angular, undefined) {
	var hola = "hola";
	console.log("cargo")
	angular.module('encubarteApp', [])

.controller('registroController', ['$scope', function($scope){

		$scope.hola = "hola";
		console.log("hola");



}]);
} )(window, window.angular)

