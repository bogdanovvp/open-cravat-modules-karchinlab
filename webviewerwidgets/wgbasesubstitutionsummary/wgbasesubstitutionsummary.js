var widgetName = 'basesubstitutionsummary';
widgetGenerators[widgetName] = {
    'info': {
        'name': 'Base Substitution',
        'width': 780, 
        'height': 400, 
        'callserver': true,
        'function': function (div, data) {
            if (div != null) {
                emptyElement(div);
            }

            // 6 colors since we have 6 categories of base changes
            var colorPalette = [
                '#CF212D',
                '#1439CC',
                '#0EB554',
                '#70119C',
                '#D1941B',
                '#E57CEB',
            ];

            div.style.width = 'calc(100% - 37px)';
            div.style.marginTop = '15px';
            var chartDiv = getEl('canvas');
            chartDiv.style.width = 'calc(100% - 20px)';
            chartDiv.style.height = 'calc(100% - 20px)';
            addEl(div, chartDiv);
            var x = [];
            var y = [];
            
            // "invisible" bars separating regular bars from bars representing base change category
            var blankSpace = [];
            blankSpace.length = 96;
            blankSpace.fill(-2.6);
            
            // bars representing base change category
            var baseChangeCategory = [];
            baseChangeCategory.length = 96;
            baseChangeCategory.fill(-0.4);

            var lineHorizontalZero = [];
            lineHorizontalZero.length = 96;
            lineHorizontalZero.fill(0);

            let substitutionData = data[0];
            let numSubstitutions = data[1];

            var colors = [];

            let i = 0;
            for (baseChange in substitutionData) {
                for (triplet in substitutionData[baseChange]) {
                    x.push(triplet);
                    y.push(substitutionData[baseChange][triplet] / numSubstitutions * 100);
                    colors.push(colorPalette[i % colorPalette.length]);
                }
                i++;
            }

            var secondaryXAxisLabels = ['A>C', 'A>G', 'A>T', 'G>C', 'G>A', 'G>T'];
            var secXAxisLabelIndex = 0;
            var tripletLabelIndex = 0;
            
            var chart = new Chart(chartDiv, {
                type: 'bar',
                data: {
                    borderColor: 'black',
                    labels: x,
                    datasets: [
                        {
                            data: y,
                            backgroundColor: colors,
                            borderColor: colors,
                            borderWidth: 0.7,
                            hoverBorderColor: '#aaaaaa',
                            xAxisID: 'triplets'
                        },
                        {
                            data: blankSpace,
                            fill: false,
                            backgroundColor: 'rgba(255,10,13,0)',
                            borderColor: 'rgba(255,10,13,0)',
                            borderWidth: 0,
                            hoverBorderColor: '#aaaaaa',
                            xAxisID: 'triplets'
                        },
                        {
                            data: baseChangeCategory,
                            backgroundColor: colors,
                            borderColor: colors,
                            borderWidth: 0.7,
                            hoverBorderColor: '#aaaaaa',
                            xAxisID: 'triplets'
                        },
                        {
                            data: lineHorizontalZero,
                            type: 'line',
                            backgroundColor: 'black',
                            borderColor: 'black',
                            borderWidth: 1,
                            pointRadius: 0,
                            pointHoverRadius: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: { display: false },
                    scales: {
                        xAxes: [
                            {
                                stacked: true,
                                id: 'triplets',
                                scaleLabel: { display: true },
                                ticks: {
                                    beginAtZero: true,
                                    stepSize: 1.0,
                                    maxRotation: 90,
                                    minRotation: 90,
                                    fontSize: 6,
                                    fontColor: 'black',
                                    padding: -25
                                },
                                gridLines: {
                                    drawBorder: false,
                                    drawOnChartArea: false,
                                    tickMarkLength: 0,
                                }
                            },
                            {
                                stacked: true,
                                id: 'baseChanges',
                                scaleLabel: { display: true },
                                ticks: {
                                    callback:function() {
                                        tripletLabelIndex++;
                                        if ((tripletLabelIndex % 16 == 8) && tripletLabelIndex > 96) {
                                            if (secXAxisLabelIndex == 6) {secXAxisLabelIndex = 0;}
                                            secXAxisLabelIndex++;
                                            return secondaryXAxisLabels[secXAxisLabelIndex - 1];
                                        }
                                    },
                                    beginAtZero: true,
                                    stepSize: 1.0,
                                    autoSkip: false,
                                    maxRotation: 0,
                                    minRotation: 0,
                                    fontSize: 16,
                                    fontColor: 'black',
                                    padding: -19, 
                                },
                                gridLines: {
                                    drawBorder: false,
                                    drawOnChartArea: false,
                                    tickMarkLength: 0,
                                }
                            }
                        ],
                        yAxes: [
                            {
                                stacked: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Percentage of Mutations',
                                    fontSize: 16,
                                    fontColor: 'black'
                                },
                                ticks: {
                                    fontSize: 16,
                                    fontColor: 'black',
                                    beginAtZero: true,
                                    min: -3,
                                },
                                afterBuildTicks: function(chart) {    
                                    chart.ticks.pop(); 
                                },
                                gridLines: {
                                    drawOnChartArea: false,
                                    zeroLineColor: 'black',
                                    color: 'black'
                                },
                            },
                        ],
                    },
                    tooltips: {
                        backgroundColor: '#ffffff',
                        displayColors: false,
                        titleFontColor: '#000000',
                        titleFontStyle: 'normal',
                        bodyFontColor: '#000000',
                        borderColor: '#333333',
                        borderWidth: 1,
                        filter: function (tooltipItem) {
                            return (tooltipItem.datasetIndex == 0);
                        }
                    },
                }
            });
        }
    }
};