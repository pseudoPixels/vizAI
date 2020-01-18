$(document).ready(function(){

    alert($("#names").text());

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

    function re_draw_graph() {

                var graph_x_axis = $("#graph_x_axis").text();
                var graph_y_axis = $("#graph_y_axis").text();
                var graph_color = $("#graph_color").text();
                var graph_facet = $("#graph_facet").text();
                var graph_size = $("#graph_size").text();
                var graph_names = $("#names").text();

                var chart_type = $("#chart_type").val();
                var chart_template = $("#chart_template").val();

                $.ajax({
                    type: "POST",
                    cache: false,
                    url: "/getPlot",
                    data: "graph_x_axis="+graph_x_axis+
                           "&graph_y_axis="+graph_y_axis+
                           "&graph_color="+graph_color+
                           "&graph_facet="+graph_facet+
                           "&graph_size="+graph_size+
                           "&graph_names="+graph_names+
                           "&chart_type="+chart_type+
                           "&chart_template="+chart_template,
                    success: function (option) {
                        //alert(option['plotData']);
                        var figure = JSON.parse(option['plotData']);
                        Plotly.newPlot('myDiv', figure.data, figure.layout);

                        var chart_params = option['chart_params'];
                        for (aParam of chart_params) {
                            $("#"+aParam).show();
                        }
                    },
                    error: function (xhr, status, error) {
                            alert(xhr.responseText);
                    }

                });
    }

    $(document).on("change", "#chart_type, #chart_template", function(){
          re_draw_graph();
    });

    $(".aFeature").draggable({
        helper:'clone'
    });

    $(".featureDroppable").droppable({
        accept:'.aFeature',
        classes: {
            "ui-droppable-active": "ui-state-default"
        },
        drop: function(ev, ui){
            var droppedItem = $(ui.draggable).clone();
            $(this).html($(ui.draggable).text());
            re_draw_graph();


        }

    });

});