$(document).ready(function () {
    $(".imgExportSettings").on('change', function () {

        // alert($("#project_id").text());

        var baseURL = "/download_images_as_zip/" + $("#project_id").text();
        var height = $("#imgHeight").val();
        var width = $("#imgWidth").val();
        var extension = $("#imgExtension").val();

        var targetURL = baseURL + "/" + width + "/" + height + "/" + extension;

        $("#expLink").prop('href', targetURL);
    });


    $.ajax({
        type: "POST",
        cache: false,
        url: "/getFavouritesViz/" + $('#project_id').text(),
        success: function (option) {
            // No plots added to the favourites yet. Show this message to the user
            if (Object.keys(option['plots']).length == 0) {
                $("#alertEmptyFav").show();
            }
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
        }

    });

});