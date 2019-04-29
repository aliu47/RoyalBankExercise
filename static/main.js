var app = angular.module('myApp', ["ui.grid"]);
// Directive for generic chart, pass in chart options
app.directive('hcChart', function () {
    return {
        restrict: 'E',
        template: '<div></div>',
        scope: {
            options: '='
        },
        link: function ($scope, element) {

            var chart = Highcharts.chart(element[0], $scope.options);

            $scope.$watch('options', function (newVal) {
                if (newVal) {
                    chart.update($scope.options);
                }
            }, true);
        }
    }
})
app.config(['$locationProvider', function ($locationProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
}])
//need to change {{}} to {a  a} because of angular and Jinja2 conflict
app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
}])
    //Controller for graph page
    .controller('homeCtrl', function ($scope, $http) {
        $scope.sortOption = ["Source_System", "Management_Owner"];
        $scope.chartOptions = {
            chart: {
                type: 'column',
            },
            title: {
                text: 'GRM ISSUE'
            },
            xAxis: {
                categories: ['ABC System', 'BCD System', 'CDE System', 'DEF System', 'EFG System', 'FGH System']
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true
                    },
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function () {
                                $scope.focusData(this);
                            }
                        }
                    }
                }
            },
            series: [{
                name: '2019-02-28',
                data: [0, 0, 0, 0, 0, 0],
            }, {
                name: '2019-03-31',
                data: [0, 0, 0, 0, 0, 0],
            }]
        }
        //default to source Graph
        $scope.choice = $scope.sortOption[0];
        Sort($scope.choice);
        $scope.optionSelect = function (choice) {
            console.log(choice);
            if (choice == $scope.sortOption[0]) {
                category = ['ABC System', 'BCD System', 'CDE System', 'DEF System', 'EFG System', 'FGH System']
                Sort(choice, category);
            }
            else if (choice == $scope.sortOption[1]) {
                category = ['Owner1', 'Owner2', 'Owner3', 'Owner4', 'Owner5', 'Owner6']
                Sort(choice, category);

            }
        };
        //Redirect the user for more info about graph element
        $scope.focusData = function (current) {
            param = current.category;
            param = param.replace(' ', '_');
            date = current.series.name;
            param = param.replace('_System', "");
            $scope.values = $scope.choice + "=" + param + "&asofdate=" + date;
            window.open("./about/" + $scope.values, '_blank');

        }
        function Sort(choice, category) {
            try {
                $http.get("http://localhost:5000/dataCount?asofdate&" + choice)
                    .then(function (response) {
                        var data = response.data;
                        var data = data.data;
                        var febData = [], marData = [];
                        for (let index = 0; index < data.length; index++) {
                            date = data[index].asofdate;
                            system = data[index][choice];
                            count = data[index].counts;
                            if (date.includes("2019-02-28")) {
                                febData[index] = count;
                            }
                            else if (date.includes("2019-03-31")) {
                                marData[index] = count;
                            }
                        }
                        $scope.chartOptions = {
                            xAxis: {
                                categories: category
                            },
                            series: [{
                                name: '2019-02-28',
                                data: [febData[0], febData[1], febData[2], febData[3], febData[4], febData[5]],
                            }, {
                                name: '2019-03-31',
                                data: [marData[6], marData[7], marData[8], marData[9], marData[10], marData[11]],
                            }]
                        }
                    })
            } catch (err) {
                console.log("Error getting data");
            }
        }
    })
    //Controller for specific table
    .controller('focusCtrl', function ($scope, $http, $location,) {
        $scope.gridOptions = {};
        // maximum rows that can be rendered outside of the view
        $scope.gridOptions.excessRows=100;
        //read data from url to make GET request
        var url = $location.url();
        url = url.replace(/(about)/g, "");
        url = url.replace(/([/])/g, '');
        
        $http.get("http://localhost:5000/dataSort?" + url)
            .then(function (response) {
                var data = response.data;
                sheetData = data.data;
                $scope.gridOptions = {
                    data: sheetData,
                }
                console.log(sheetData.length);
            })

    });