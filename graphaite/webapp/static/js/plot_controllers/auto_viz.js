$(document).ready(function(){

    function get_uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        });
    }

    $.ajax({
        type: "POST",
        cache: false,
        url: "/getAutoViz",
        success: function (option) {
            for (aPlotID in option['plots']){
                // {'figure_data':'jsonFigureValue', 'feature_tags':['feature1', 'feature2',..]}
                aPlotObject = option['plots'][aPlotID]; 
                
                //add the plot to the auto viz tabs, as per the figure tags
                for (index = 0; index < aPlotObject['feature_tags'].length; index++){    
                    aFeatureTag = aPlotObject['feature_tags'][index];
                    // create unique div id, to map the plotly fig
                    var unique_div_id = get_uuid();
                    $("#tab-row-"+aFeatureTag).append("<div class='col-lg-6' style='width:100%;'>\
                                                            <div class='card' >\
                                                                <div class='card-body'>\
                                                                    <h4 class='card-title box-title'>"+ aPlotObject['feature_tags'].join(" | ") +"</h4>\
                                                                    <div id='" + unique_div_id + "' style='width:650px;'></div>\
                                                                    <div><a href='#'>Edit chart</a> | <a href='#'>Add insights</a> | <a href='#'>Add to data story</a> | <a href='#'>Delete</a> </div>\
                                                                </div>\
                                                            </div>\
                                                        </div>");

                    var figure = JSON.parse(aPlotObject['figure_data']);
                    Plotly.newPlot(unique_div_id, figure.data, figure.layout);
                }

                
            }
        },
        error: function (xhr, status, error) {
                alert(xhr.responseText);
        }

    });

});
