function showStatus(result) {

   // need to extract jsonify object
   // console.log("inside show status");
   // console.log(result);


    if ( result['app_pending'] !== "" ) {
        $("#application_pending").html(result['app_pending']);
        $("#submit").val('Application Review');

   } if ( result['app_review'] !== "" ) {
        $("#application_review").html(result['app_review']);
        $("#submit").val('Application Result');
    } if ( result['app_results'] !== "" ){
        $("#application_results").html(result['app_results']);
        $("#submit").hide();
        $("#textarea").hide();

    } 
}

  
function setStatus(evt) {
    if (evt) {
        evt.preventDefault();
    }

    // console.log('inside setStatus');

    // fetch dictionary 
    let formValues = {
        "submit": $("#submit").val(),
        "textbox": $("#textbox").val()
    }

    // console.log(formValues);

    // fetch dictionary 

    let filledFormId = $("#filled_form_id").val();
    // console.log(filledFormId);


    $.post("/app-status/" + filledFormId, formValues, getStatus);
}

function getStatus() {


    // console.log("inside get status");

    let filledFormId = $("#filled_form_id").val();

    $.get("/app-status/" + filledFormId, showStatus);

}

$("#app_form_status").on("submit", setStatus);
getStatus();
