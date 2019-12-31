$(document).ready(function(){


    $(document).on('change', ".plot_feature" ,function () {//here
    	$.ajax({
            type: "POST",
            cache: false,
            url: "/getPlot",
            data: "color="+$(this).val(),
            success: function (option) {
                //alert(option['plotData']);
                var figure = JSON.parse(option['plotData']);
                Plotly.newPlot('myDiv', figure.data, figure.layout);
            },
            error: function (xhr, status, error) {
                    alert(xhr.responseText);
            }

    	});


    });



    $( ".aFeature" ).draggable({helper:'clone'});

    $(".featureDroppable").droppable({
        accept:'.aFeature',
        classes: {
            "ui-droppable-active": "ui-state-default"
        },
        drop: function(ev, ui){
            var droppedItem = $(ui.draggable).clone();
            $(this).html($(ui.draggable).text());

            var graph_x_axis = $("#graph_x_axis").text();
            var graph_y_axis = $("#graph_y_axis").text();
            var graph_color = $("#graph_color").text();
            var graph_facet = $("#graph_facet").text();
            var graph_size = $("#graph_size").text();

            $.ajax({
                type: "POST",
                cache: false,
                url: "/getPlot",
                data: "graph_x_axis="+graph_x_axis+"&graph_y_axis="+graph_y_axis+"&graph_color="+graph_color+"&graph_facet="+graph_facet+"&graph_size="+graph_size,
                success: function (option) {
                    //alert(option['plotData']);
                    var figure = JSON.parse(option['plotData']);
                    Plotly.newPlot('myDiv', figure.data, figure.layout);
                },
                error: function (xhr, status, error) {
                        alert(xhr.responseText);
                }

    	    });

        }

    });

});