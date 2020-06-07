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


});