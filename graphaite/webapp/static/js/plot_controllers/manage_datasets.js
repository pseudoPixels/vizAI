$(document).ready(function (e) {

    var dTable = NaN;
    var already = false;


    function update_dataset() {


        $.ajax({
            url: 'http://127.0.0.1:5000/getDataFrame/' + $('#project_id').text(), // point to server-side URL
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
                        columns: data.columns

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
            url: 'http://127.0.0.1:5000/python-flask-files-upload/' + $('#project_id').text(),
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


            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            }
        });
    });




});