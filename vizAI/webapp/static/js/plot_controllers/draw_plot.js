$(document).ready(function(){


    $(document).on('change', ".plot_feature" ,function () {//here
        //alert($(this).val());

        //get the ouput list via async call
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

});