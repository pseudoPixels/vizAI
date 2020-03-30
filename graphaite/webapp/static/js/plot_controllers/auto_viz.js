$(document).ready(function(){

        plotCounter = -1;

    	$.ajax({
            type: "POST",
            cache: false,
            url: "/getAutoViz",
            success: function (option) {
                $("#r").append("<div id='myDiv' style='width:48%;'></div>");
                var figure = JSON.parse(option['plotData']);
                Plotly.newPlot('myDiv', figure.data, figure.layout);
            },
            error: function (xhr, status, error) {
                    alert(xhr.responseText);
            }

    	});






    	function start_long_task() {
            // add task status elements
            div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
            $('#progress').append(div);

            // create a progress bar
            var nanobar = new Nanobar({
                bg: '#44f',
                target: div[0].childNodes[0]
            });

            // send ajax POST request to start background job
            $.ajax({
                type: 'POST',
                url: '/longtask',
                success: function(data, status, request) {
                    status_url = request.getResponseHeader('Location');
                    update_progress(status_url, nanobar, div[0]);
                },
                error: function() {
                    alert('Unexpected error');
                }
            });
        }
        function update_progress(status_url, nanobar, status_div) {
            // send GET request to status URL
            $.getJSON(status_url, function(data) {
               if (data['state'] == 'PLOTDONE') {
                    if ('result' in data) {

                        current = parseInt(data['current']);
                        alert(current.toString() + " => " + plotCounter.toString());
                        if (current > plotCounter){
                            $("#r").append("<div id='"+ data['plotid']+ "' style='width:48%;'></div>");
                            var figure = JSON.parse(data['result']);
                            Plotly.newPlot(data['plotid'], figure.data, figure.layout);
                            plotCounter = plotCounter + 1;
                        }

                    }

                     setTimeout(function() {
                        update_progress(status_url, nanobar, status_div);
                    }, 2000);
                }
                else {
                    // rerun in 2 seconds
                    setTimeout(function() {
                        update_progress(status_url, nanobar, status_div);
                    }, 2000);
                }
            });
        }
        $(function() {
            $('#start-bg-job').click(start_long_task);
        });

});
