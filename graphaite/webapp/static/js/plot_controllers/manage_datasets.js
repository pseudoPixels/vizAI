$(document).ready(function (e) {

    // alert(url_for('manage_datasets', project_id = project_id));
    var dTable = NaN;
    var already = false;


    function update_dataset() {


        $.ajax({
            url: '/getDataFrame/' + $('#project_id').text(), // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            type: 'post',
            success: function (data) { // display success response
                if (data.isDataAvailable == true) {
                    if (already == true) {
                        dTable.clear().draw();
                        dTable.columns.adjust().draw();
                        dTable.destroy();
                        $('#view_raw_data thead').html('');
                    } else {
                        already = true;
                    }
                    dTable = $('#view_raw_data').DataTable({
                        data: data.my_table,
                        columns: data.columns,
                        stateSave: true
                    });
                }
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });

    }

    update_dataset();



    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins == 0) {
            $('#msg').html('<span style="color:red">Select at least one file</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        $.ajax({
            url: '/python-flask-files-upload/' + $('#project_id').text(),
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            success: function (response) { // display success response
                $('#msg').html('');
                $.each(response, function (key, data) {
                    if (key !== 'message') {
                        $('#msg').append(key + ' -> ' + data + '<br/>');
                    } else {
                        $('#msg').append(data + '<br/>');
                    }
                })
                // dTable.destroy();
                update_dataset();
                get_and_render_variables();

                alert("Dataset Connected Successfully!\n\nPlease Set Feature Variables from below and Hit 'Set & Save'");

            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    });


    function get_and_render_variables() {
        $.ajax({
            url: '/get_variables/' + $('#project_id').text(),
            dataType: 'json', // what to expect back from server
            type: 'post',
            success: function (res) { // display success response
                console.log(res['target_feature'])

                //Render the dropdown for selecting target variable
                for (i = 0; i < res['categorical'].length; i++) {
                    aFeature = res['categorical'][i];
                    opt = '';
                    if (aFeature == res['target_feature']) {
                        opt = "<option value='" + aFeature + "' selected='selected'>" + aFeature + "</option>";
                    } else {
                        opt = "<option value='" + aFeature + "'>" + aFeature + "</option>";
                    }
                    $("#targetVar").append(opt);
                }

                for (i = 0; i < res['all'].length; i++) {
                    aFeature = res['all'][i];

                    rad = '';

                    if (res['selected_features'].includes(aFeature)) {
                        rad = '<input type="checkbox" value="' + aFeature + '" name="selected_features" checked> ' + aFeature + '</input><br/>';
                    } else {
                        rad = '<input type="checkbox" value="' + aFeature + '" name="selected_features"> ' + aFeature + '</input><br/>';
                    }

                    $("#selectVar").append(rad);

                }



            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    }

    get_and_render_variables();



    function set_feature_and_target_variables() {

        $.ajax({
            type: "POST",
            cache: false,
            url: "/set_variables/" + $('#project_id').text(),
            data: $('#fs').serialize(),
            success: function (option) {
                alert("Feature and Target Variables Set and Saved.");
            },
            error: function (xhr, status, error) {
                alert(xhr.responseText);
            }
        });
    }


    $("#save_feature_info").on("click", function () {
        set_feature_and_target_variables();
    });

});

// http://127.0.0.1:5000