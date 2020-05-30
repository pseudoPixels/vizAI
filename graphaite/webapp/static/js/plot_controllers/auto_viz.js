$(document).ready(function () {

    function get_uuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function show_only_selected_feature_tabs() {
        //1. first hide all the tabs as init
        $("input[type=checkbox][name=selected_features]").each(function () {
            $("#custom-nav-" + $(this).val() + "-tab").hide();

        });

        //2. show only the select feature tabs
        $('input[type=checkbox][name=selected_features]:checked').each(function () {
            $("#custom-nav-" + $(this).val() + "-tab").show();

        });

        //3. click on one of the feature tab, so that the visulations are visible to user. 
        $("#custom-nav-" + $('input[type=checkbox][name=selected_features]:checked').val() + "-tab").click();
    }

    function get_auto_vizuations() {
        // disable the ai generation button, so there is only single requests at any given time
        // the button is enabled again on completion of the request.
        $('#btn_get_auto_vis').prop('disabled', true);
        $('.aiProgressStatus').show();

        $.ajax({
            type: "POST",
            cache: false,
            url: "http://127.0.0.1:5000/getAutoViz/" + $('#project_id').text(),
            data: $('#fs').serialize(),
            success: function (option) {
                for (aPlotID in option['plots']) {
                    // {'figure_data':'jsonFigureValue', 'feature_tags':['feature1', 'feature2',..]}
                    aPlotObject = option['plots'][aPlotID];

                    //add the plot to the auto viz tabs, as per the figure tags
                    for (index = 0; index < aPlotObject['feature_tags'].length; index++) {
                        aFeatureTag = aPlotObject['feature_tags'][index];
                        // create unique div id, to map the plotly fig
                        var unique_div_id = get_uuid();
                        var graphEditorLink = "http://127.0.0.1:5000/graph_editor/" + $('#project_id').text() + "/" + aPlotObject['graph_id'];

                        var favourtieBtnIcon = '';

                        if (aPlotObject['isFavourite'] == true) {
                            favourtieBtnIcon = "<i class='menu-icon fa fa-star' style='color:orange;align:right;float:right; font-size: 24px;'></i>"
                        } else {
                            favourtieBtnIcon = "<i class='menu-icon fa fa-star-o' style='color:orange;align:right;float:right; font-size: 24px;'></i>"
                        }


                        $("#tab-row-" + aFeatureTag).append("<div class='col-lg-6' style='width:100%;'>\
                                                                <div class='card' >\
                                                                    <div class='card-body'>\
                                                                    <span style='width:100%'> <span class='card-title box-title'>"+ aPlotObject['feature_tags'].join(" | ") + "</span>" + "<a href='#' class='addToFavourite' \
                                                                    projectID='" + $('#project_id').text() + "' graphID='" + aPlotObject['graph_id'] + "' title='Add/Remove Fabourtie' >" + favourtieBtnIcon + "</a></span> \
                                                                        <div id='" + unique_div_id + "' style='width:650px;'></div>\
                                                                        <div><a href='" + graphEditorLink + "'>Edit chart</a> \
                                                                         | <a href='#'>Add insights</a> \
                                                                         | <a href='#' class='addToFavourite' projectID='" + $('#project_id').text() + "' graphID='" + aPlotObject['graph_id'] + "' >Add to Favourties</a> \
                                                                         | <a href='#'>Delete</a> </div>\
                                                                    </div>\
                                                                </div>\
                                                            </div>");

                        var figure = JSON.parse(aPlotObject['figure_data']);
                        Plotly.newPlot(unique_div_id, figure.data, figure.layout);
                    }
                }

                // show only the selected featrues of visualizations
                show_only_selected_feature_tabs();

            },
            error: function (xhr, status, error) {
                alert(xhr.responseText);
            },
            complete: function () {
                //enable the request button on completion of the request, regardless of the request failure/success.
                $('#btn_get_auto_vis').prop('disabled', false);
                $('.aiProgressStatus').hide();
            }

        });
    }


    function add_graph_to_favourite(projectID, graphID, favIcon) {
        $.ajax({
            type: "POST",
            cache: false,
            url: "http://127.0.0.1:5000/add_or_remove_graph_to_favourite/",
            data: "projectID=" + projectID + '&graphID=' + graphID,
            success: function (returnData) {
                console.log("added graph to favourites");


                if (returnData['statusCode'] == 1) {
                    favIcon.removeClass("fa-star-o");
                    favIcon.addClass("fa-star");
                    // alert("Graph Added to Favourite.")

                } else if (returnData['statusCode'] == -1) {
                    favIcon.removeClass("fa-star");
                    favIcon.addClass("fa-star-o");
                    // alert("Graph Removed from Favourite!")
                } else {
                    alert("Something went wrong!!!")
                }

            },
            error: function (xhr, status, error) {
                alert(xhr.responseText);
            }

        });
    }





    // =======================================================
    // UI Interactions Handlers
    //========================================================

    $("#btn_get_auto_vis").on("click", function () {
        get_auto_vizuations();
    });

    $(document).on("click", ".addToFavourite", function () {
        console.log($(this).attr("projectID"));
        console.log($(this).attr("graphID"));
        var favIcon = $(this).find('i')

        add_graph_to_favourite($(this).attr("projectID"), $(this).attr("graphID"), favIcon);

        return false;
    });








    // on page load, get the available visualziation present by default.
    get_auto_vizuations();

});
