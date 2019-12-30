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
        drop: function(ev, ui){
            var droppedItem = $(ui.draggable).clone();
            $(this).html("<h4><b>"+$(ui.draggable).text()+"</b></h4>");

            $.ajax({
                type: "POST",
                cache: false,
                url: "/getPlot",
                data: "color="+$(ui.draggable).text(),
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