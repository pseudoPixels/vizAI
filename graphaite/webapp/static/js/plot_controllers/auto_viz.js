$(document).ready(function(){

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

});
