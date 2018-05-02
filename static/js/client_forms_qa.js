function showStatusChanged(results) {
   // need to extract jsonify object
   console.log($("#dropdown").val());


   if ($("#dropdown").val() == 'app_pending'){
        $("#application_pending").html(results);
   }else if ($("#dropdown").val() == 'app_review'){
        $("#application_review").html(results);
   }else{

        $("#application_results").val(results);
   }

}
  

    // alert("Client's form status has been changed");



function getStatusInfo(evt) {
    evt.preventDefault();

    let formValues = {
        "dropdown": $("#dropdown").val(),
        "textbox": $("#textbox").val()
    }

    let filledFormId = $("#filled_form_id").val();


    $.post("/advocate/" + filledFormId, formValues, showStatusChanged);
}

$("#app_form_status").on("submit", getStatusInfo);