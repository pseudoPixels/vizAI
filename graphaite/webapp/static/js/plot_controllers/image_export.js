
$(".imgExportSettings").on('change', function () {

    // alert($("#project_id").text());

    var baseURL = "http://127.0.0.1:5000/download_images_as_zip/" + $("#project_id").text();
    var height = $("#imgHeight").val();
    var width = $("#imgWidth").val();
    var extension = $("#imgExtension").val();

    var targetURL = baseURL + "/" + width + "/" + height + "/" + extension;

    $("#expLink").prop('href', targetURL);
});