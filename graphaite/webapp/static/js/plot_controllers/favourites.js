$(document).ready(function () {

    function get_uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }


    $.ajax({
        type: "POST",
        cache: false,
        url: "http://127.0.0.1:5000/getFavouritesViz/" + $('#project_id').text(),
        success: function (option) {
            // check if the plots in favourites are not empty
            if (Object.keys(option['plots']).length > 0) {
                for (aPlotID in option['plots']) {
                    // {'figure_data':'jsonFigureValue', 'feature_tags':['feature1', 'feature2',..]}
                    aPlotObject = option['plots'][aPlotID];

                    // create unique div id, to map the plotly fig
                    var unique_div_id = get_uuid();
                    var graphEditorLink = "http://127.0.0.1:5000/graph_editor/" + $('#project_id').text() + "/" + aPlotObject['graph_id'];
                    $("#favsViz").append("<div class='col-lg-6' style='width:80%;'>\
                                                                    <div class='card' >\
                                                                        <div class='card-body'>\
                                                                            <span style='width:100%'> <span class='card-title box-title'>"+ aPlotObject['feature_tags'].join(" | ") + "</span> <i class='menu-icon fa fa-star' style='color:orange;align:right;float:right; font-size: 24px;'></i> </span> \
                                                                            <div id='" + unique_div_id + "' style='width:650px;'></div>\
                                                                            <div><a target='_blank' href='" + graphEditorLink + "'>Edit chart</a> | <a href='#'>Add insights</a> | <a href='#'>Remove from Favourites</a> </div>\
                                                                        </div>\
                                                                    </div>\
                                                                </div>");

                    var figure = JSON.parse(aPlotObject['figure_data']);
                    Plotly.newPlot(unique_div_id, figure.data, figure.layout);
                }

            }
            // No plots added to the favourites yet. Show this message to the user
            else {
                $("#favsViz").append("<h3 style='align:center;'>No Graphs added to favourites yet! <br/><br/> Select graphs from the <i>'Auto Plots (AI)'</i> menu to appear here.</h3>");
            }





        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }

    });





});
