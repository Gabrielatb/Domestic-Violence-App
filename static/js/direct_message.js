function messagePostComplete(result) {
    alert("message sent")

}







  function postMessage(evt) {
    if (evt) {
        evt.preventDefault();
    }
    // console.log("inside post message");
//     // console.log('inside setStatus');

//     // fetch dictionary 
    let formValues = {
        "textarea": $("#textarea").val()
    }

    console.log(formValues);
//     // console.log(formValues);

//     // fetch dictionary 

//     let filledFormId = $("#filled_form_id").val();
//     // console.log(filledFormId);


    $.post('/message',  formValues, messagePostComplete);
// }

// function getStatus() {


//     // console.log("inside get status");

//     let filledFormId = $("#filled_form_id").val();

//     $.get("/app-status/" + filledFormId, showStatus);

}

$("#direct_message_form").on("submit", postMessage);
// getStatus();

