var widgetName = 'mutationsignature';
widgetGenerators[widgetName] = {
	'info': {
		'name': 'Mutation Signature',
		'width': 800, 
		'height': 510, 
        'callserver': true,
		'function': function (div, data) {
			if (div != null) {
                emptyElement(div);
            }

            div.style.textAlign = 'center';
            div.style.width = 'calc(100% - 37px)';
            
            let substitutionData = data[0];
            let numSubstitutions = data[1];

            // create SVG
            var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

            /*$("#detailwidget_info_mutationsignature").resize(function() {
                var width = this.style.width;
                var height = this.style.height;
                svg.setAttribute('width', width);
                svg.setAttribute('height', height);
                console.log(svg.width.animVal.value);
            }
            );*/

            svg.setAttribute('width', '800');
            svg.setAttribute('height', '460');
            svg.style.height = '460';
            svg.style.width = '800';
            svg.preserveAspectRatio = "none";

            // draw x-axis
            var xAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            xAxis.setAttribute('x1', '70');
            xAxis.setAttribute('y1', '370');
            xAxis.setAttribute('x2', '750');
            xAxis.setAttribute('y2', '370');
            xAxis.setAttribute('stroke', 'black');
            xAxis.style.strokeWidth = '.15em';

            // draw triplet labels on x axis
            var xTripletLabel = 85;
            var yTripletLabel = 390;
            for (baseChange in substitutionData) {
                for (triplet in substitutionData[baseChange]) {
                    var tripletLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    tripletLabel.setAttribute('x', xTripletLabel);
                    tripletLabel.setAttribute('y', yTripletLabel);
                    tripletLabel.style.fontSize = '7px';
                    tripletLabel.setAttribute('transform', 'rotate(270,' + xTripletLabel + ',' + yTripletLabel + ')');
                    var base1 = document.createElementNS("http://www.w3.org/2000/svg","tspan");
                    base1.textContent = triplet.charAt(0);
                    base1.setAttribute('fill', 'black');
                    base1.style.fontSize = '7px';
                    base1.style.stroke = 'black';
                    base1.style.strokeWidth = '0.05em';
                    tripletLabel.appendChild(base1);

                    var redMiddleBase = document.createElementNS("http://www.w3.org/2000/svg","tspan");
                    redMiddleBase.textContent = triplet.charAt(1);
                    redMiddleBase.setAttribute('fill', 'red');
                    redMiddleBase.style.fontSize = '7px';
                    redMiddleBase.style.stroke = 'red';
                    redMiddleBase.style.strokeWidth = '0.05em';
                    tripletLabel.appendChild(redMiddleBase);

                    var base3 = document.createElementNS("http://www.w3.org/2000/svg","tspan");
                    base3.textContent = triplet.charAt(2);
                    base3.setAttribute('fill', 'black');
                    base3.style.fontSize = '7px';
                    base3.style.stroke = 'black';
                    base3.style.strokeWidth = '0.05em';
                    tripletLabel.appendChild(base3);

                    svg.appendChild(tripletLabel);
                    xTripletLabel += 7;
                }
            }

            // draw base change labels
            var secondaryXAxisLabels = ['A>C', 'A>G', 'A>T', 'G>C', 'G>A', 'G>T'];
            var xBaseChangeLabel = 120;
            var yBaseChangeLabel = 420;
            for (label of secondaryXAxisLabels) {
                var baseChangeLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                baseChangeLabel.setAttribute('x', xBaseChangeLabel);
                baseChangeLabel.setAttribute('y', yBaseChangeLabel);
                baseChangeLabel.setAttribute('fill', 'black');
                baseChangeLabel.style.fontSize = '18px';
                baseChangeLabel.style.stroke = 'black';
                baseChangeLabel.style.strokeWidth = '0.03em';
                baseChangeLabel.textContent = label;
                svg.appendChild(baseChangeLabel);
                xBaseChangeLabel += 110;
            }

            var baseChangeTitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            baseChangeTitle.textContent= 'Base Change';
            baseChangeTitle.setAttribute('x', 370);
            baseChangeTitle.setAttribute('y', 450);
            baseChangeTitle.style.fontSize = '18px';
            baseChangeTitle.style.stroke = 'black';
            baseChangeTitle.style.strokeWidth = '0.03em';
            svg.appendChild(baseChangeTitle);

            // draw colored bars above base change labels
            var baseChangeBarColors = ['red', 'blue', 'green', 'purple', 'orange', 'pink'];
            var xBaseChangeBar = 80;
            var colorIndex = 0;
            for (let i = 0; i < 6; i++) {
                var baseChangeBar = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                baseChangeBar.setAttribute('x', xBaseChangeBar);
                baseChangeBar.setAttribute('y', '400');
                baseChangeBar.setAttribute('width', '110');
                baseChangeBar.setAttribute('height', '4');
                baseChangeBar.setAttribute('fill', baseChangeBarColors[colorIndex]);
                baseChangeBar.setAttribute('stroke', baseChangeBarColors[colorIndex]);
                svg.appendChild(baseChangeBar);
                xBaseChangeBar += 112;
                colorIndex++;
            }

            // draw y-axis
            var yAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            var yAxisMaxCor = '370';
            var yAxisMinCor = '15';
            yAxis.setAttribute('x1', '80');
            yAxis.setAttribute('y1', yAxisMinCor);
            yAxis.setAttribute('x2', '80');
            yAxis.setAttribute('y2', yAxisMaxCor);
            yAxis.setAttribute('stroke', 'black');
            yAxis.style.strokeWidth = '.15em';

            // draw y-axis title
            var yAxisTitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            yAxisTitle.setAttribute('x', '25');
            yAxisTitle.setAttribute('y', '300');
            yAxisTitle.setAttribute('fill', 'black');
            yAxisTitle.setAttribute('transform', 'rotate(270, 25, 300)');
            yAxisTitle.textContent = 'Percentage of Mutations (%)';
            yAxisTitle.style.fontSize = '18px';
            yAxisTitle.style.stroke = 'black';
            yAxisTitle.style.strokeWidth = '0.03em';

            var x = 70;
            var yTickLine = 15;
            var yTickLabel = 20;

            var percentages = [];
            
            for (baseChange in substitutionData) {
                for (triplet in substitutionData[baseChange]) {
                    percentages.push(substitutionData[baseChange][triplet] / numSubstitutions * 100);
                }
            }
            
            // round the max number to the nearest 5
            var maxYTick = Math.ceil(Math.max(...percentages) / 5) * 5;

            // draw y-axis ticks and tick labels
            var numTicks = maxYTick / 5;
            var currYLabel = maxYTick;
            for (let i = 0; i < numTicks; i++) {
                var tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                tick.setAttribute('x1', x);
                tick.setAttribute('y1', yTickLine);
                tick.setAttribute('x2', 80);
                tick.setAttribute('y2', yTickLine);
                tick.setAttribute('stroke', 'black');
                tick.style.strokeWidth = '.15em';
                svg.appendChild(tick);
                var tickLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                if (currYLabel < 10) {
                    tickLabel.setAttribute('x', '53');
                } else if (currYLabel == 100) {
                    tickLabel.setAttribute('x', '33');
                } else {
                    tickLabel.setAttribute('x', '43');
                }
                tickLabel.setAttribute('y', yTickLabel);
                tickLabel.setAttribute('fill', 'black');
                tickLabel.style.fontSize = '18px';
                tickLabel.style.stroke = 'black';
                tickLabel.style.strokeWidth = '0.03em';
                tickLabel.textContent = currYLabel;
                svg.appendChild(tickLabel);
                
                // length of y axis is (currently) 355
                yTickLine += 355 / numTicks;
                yTickLabel += 355 / numTicks;
                currYLabel -= 5;
            }

            // draw data on chart
            var lengthYAxis = yAxisMaxCor - yAxisMinCor;
            var xTripletBar = 80;
            var yTripletBar = 30;
            var pixelsPerYTickUnit = lengthYAxis / maxYTick;
            colorIndex = 0;
            for (let i = 0; i < percentages.length; i++) {
                var tripletBar = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                yTripletBar = parseInt(yAxisMinCor) + pixelsPerYTickUnit * (maxYTick - percentages[i]);
                var barHeight = lengthYAxis - yTripletBar + parseInt(yAxisMinCor);
                tripletBar.setAttribute('x', xTripletBar);
                tripletBar.setAttribute('y', yTripletBar);
                tripletBar.setAttribute('width', '5');
                tripletBar.setAttribute('height', barHeight);
                tripletBar.setAttribute('fill', baseChangeBarColors[colorIndex]);
                tripletBar.setAttribute('stroke', baseChangeBarColors[colorIndex]);
                svg.appendChild(tripletBar);
                xTripletBar += 7;
                if (i % 16 == 15) {
                    colorIndex++;
                }
            }

            svg.appendChild(xAxis);
            svg.appendChild(yAxis);
            svg.appendChild(yAxisTitle);
            svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
            div.appendChild(svg);
		}
	}
};