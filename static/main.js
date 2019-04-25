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
        sourceSort();
        $scope.optionSelect = function (choice) {
            console.log(choice);
            if (choice == $scope.sortOption[0]) {
                sourceSort();
            }
            else if (choice == $scope.sortOption[1]) {
                ownerSort();

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
        //sort graph based on Management_Owner
        function ownerSort() {
            try {
                $http.get("http://localhost:5000/data")
                    .then(function (response) {
                        var data = response.data;
                        var data = data.data;
                        var febData = [0, 0, 0, 0, 0, 0], marData = [0, 0, 0, 0, 0, 0];
                        for (let index = 0; index < data.length; index++) {
                            date = data[index].asofdate;
                            system = data[index].Management_Owner;
                            if (date.includes("2019-03-31")) {
                                // marData.push(data[index])
                                if (system.includes("1"))
                                    marData[0]++;
                                if (system.includes("2"))
                                    marData[1]++;
                                if (system.includes("3"))
                                    marData[2]++;
                                if (system.includes("4"))
                                    marData[3]++;
                                if (system.includes("5"))
                                    marData[4]++;
                                if (system.includes("6"))
                                    marData[5]++;
                            }
                            if (date.includes("2019-02-28")) {
                                // febData.push(data[index]);
                                if (system.includes("1"))
                                    febData[0]++;
                                if (system.includes("2"))
                                    febData[1]++;
                                if (system.includes("3"))
                                    febData[2]++;
                                if (system.includes("4"))
                                    febData[3]++;
                                if (system.includes("5"))
                                    febData[4]++;
                                if (system.includes("6"))
                                    febData[5]++;
                            }
                        }
                        $scope.chartOptions = {

                            xAxis: {
                                categories: ['Owner1', 'Owner2', 'Owner3', 'Owner4', 'Owner5', 'Owner6']
                            },
                            series: [{
                                name: '2019-02-28',
                                data: [febData[0], febData[1], febData[2], febData[3], febData[4], febData[5]],
                            }, {
                                name: '2019-03-31',
                                data: [marData[0], marData[1], marData[2], marData[3], marData[4], marData[5]],
                            }]
                        }
                    })
            } catch (err) {
                console.log("Error getting data");
            }
        }
        //sort graph based on Source_System
        function sourceSort() {
            try {
                $http.get("http://localhost:5000/data")
                    .then(function (response) {
                        var data = response.data;
                        var data = data.data;
                        var febData = [0, 0, 0, 0, 0, 0], marData = [0, 0, 0, 0, 0, 0];
                        for (let index = 0; index < data.length; index++) {
                            date = data[index].asofdate;
                            system = data[index].Source_System
                            if (date.includes("2019-03-31")) {
                                // marData.push(data[index])
                                if (system.includes("ABC"))
                                    marData[0]++;
                                if (system.includes("BCD"))
                                    marData[1]++;
                                if (system.includes("CDE"))
                                    marData[2]++;
                                if (system.includes("DEF"))
                                    marData[3]++;
                                if (system.includes("EFG"))
                                    marData[4]++;
                                if (system.includes("FGH"))
                                    marData[5]++;
                            }
                            if (date.includes("2019-02-28")) {
                                // febData.push(data[index]);
                                if (system.includes("ABC"))
                                    febData[0]++;
                                if (system.includes("BCD"))
                                    febData[1]++;
                                if (system.includes("CDE"))
                                    febData[2]++;
                                if (system.includes("DEF"))
                                    febData[3]++;
                                if (system.includes("EFG"))
                                    febData[4]++;
                                if (system.includes("FGH"))
                                    febData[5]++;
                            }
                        }
                        $scope.chartOptions = {
                            xAxis: {
                                categories: ['ABC System', 'BCD System', 'CDE System', 'DEF System', 'EFG System', 'FGH System']
                            },
                            series: [{
                                name: '2019-02-28',
                                data: [febData[0], febData[1], febData[2], febData[3], febData[4], febData[5]],
                            }, {
                                name: '2019-03-31',
                                data: [marData[0], marData[1], marData[2], marData[3], marData[4], marData[5]],
                            }]
                        }
                    })
            } catch (err) {
                console.log("Error getting data");
            }
        }
    })
    //Controller for specific table
    .controller('focusCtrl', function ($scope, $http, $location) {
        $scope.sheetData = {}
        //read data from url to make GET request
        var url = $location.url();
        url = url.replace(/(about)/g, "");
        url = url.replace(/([/])/g, '');
        $http.get("http://localhost:5000/data?" + url)
            .then(function (response) {
                var data = response.data;
                $scope.sheetData.data = data.data;
            })
    });