$(document).ready(function(){

    	$.ajax({
            type: "POST",
            cache: false,
            url: "/getAutoViz",
            success: function (option) {
                for (aPlotID in option['plots']){
                    $("#tab-row-"+aPlotID).append("<div class='col-lg-6' style='width:100%;'><div class='card' ><div class='card-body' ><h4 class='card-title box-title'>"+ aPlotID +"</h4>            <div id='" + aPlotID + "' style='width:650px;'></div>   </div></div></div>" );
                    var figure = JSON.parse(option['plots'][aPlotID]);
                    Plotly.newPlot(aPlotID, figure.data, figure.layout);
                }
            },
            error: function (xhr, status, error) {
                    alert(xhr.responseText);
            }

    	});

});
