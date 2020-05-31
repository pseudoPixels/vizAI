$(document).ready(function () {

    function get_uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    //Get the graph id
    var GRAPH_ID = $("#graph_id").text();

    //For new graph, there is no graph id yet (i.e., None).
    //in such cases create, new unique graph_id
    if (GRAPH_ID == 'None') {
        GRAPH_ID = get_uuid();
    }



    $(document).on('change', ".plot_feature", function () {//here
        $.ajax({
            type: "POST",
            cache: false,
            url: "/getPlot",
            data: "color=" + $(this).val(),
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

        var graph_x = $("#graph_x").text();
        var graph_y = $("#graph_y").text();
        var graph_color = $("#graph_color").text();
        var graph_facet = $("#graph_facet").text();
        var graph_size = $("#graph_size").text();
        var graph_names = $("#names").text();

        var chart_type = $("#chart_type").val();
        var chart_template = $("#chart_template").val();

        $.ajax({
            type: "POST",
            cache: false,
            url: "http://127.0.0.1:5000/getPlot/" + $('#project_id').text() + "/" + GRAPH_ID,
            data: "graph_x=" + graph_x +
                "&graph_y=" + graph_y +
                "&graph_color=" + graph_color +
                "&graph_facet=" + graph_facet +
                "&graph_size=" + graph_size +
                "&graph_names=" + graph_names +
                "&chart_type=" + chart_type +
                "&chart_template=" + chart_template,
            success: function (option) {
                //alert(option['plotData']);
                var figure = JSON.parse(option['plotData']);
                Plotly.newPlot('myDiv', figure.data, figure.layout);

                var chart_params = option['chart_params'];
                for (aParam of chart_params) {
                    $("#" + aParam).show();
                }
            },
            error: function (xhr, status, error) {
                alert(xhr.responseText);
            }

        });
    }

    $(document).on("change", "#chart_type, #chart_template", function () {
        re_draw_graph();
    });

    $(".aFeature").draggable({
        helper: 'clone'
    });

    $(".featureDroppable").droppable({
        accept: '.aFeature',
        classes: {
            "ui-droppable-active": "ui-state-default"
        },
        drop: function (ev, ui) {
            var droppedItem = $(ui.draggable).clone();
            $(this).html($(ui.draggable).text());
            re_draw_graph();


        }

    });



    $("#save_viz").on("click", function () {

        var graph_x = $("#graph_x").text();
        var graph_y = $("#graph_y").text();
        var graph_color = $("#graph_color").text();
        var graph_facet = $("#graph_facet").text();
        var graph_size = $("#graph_size").text();
        var graph_names = $("#names").text();

        var chart_type = $("#chart_type").val();
        var chart_template = $("#chart_template").val();

        var graph_title = $("#graph_title").val();


        $.ajax({
            type: "POST",
            cache: false,
            url: "http://127.0.0.1:5000/getPlot/" + $('#project_id').text() + "/" + GRAPH_ID + "/true",
            data: "graph_x=" + graph_x +
                "&graph_y=" + graph_y +
                "&graph_color=" + graph_color +
                "&graph_facet=" + graph_facet +
                "&graph_size=" + graph_size +
                "&graph_names=" + graph_names +
                "&chart_type=" + chart_type +
                "&chart_template=" + chart_template +
                "&graph_title=" + graph_title,
            success: function (option) {
                alert("visualization saved!!")
            },
            error: function (xhr, status, error) {
                alert(xhr.responseText);
            }

        });
    });



});
