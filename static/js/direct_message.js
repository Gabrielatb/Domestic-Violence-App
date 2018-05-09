function messagePostComplete(result) {
    alert("message sent")

}



  function postMessage(evt) {
    if (evt) {
        evt.preventDefault();
    }
        console.log('inside postMessage');
    let formValues = {
        "textarea": $("#textarea").val()
    }

    console.log(formValues);
//     // console.log(formValues);

//     // fetch dictionary 

//     let filledFormId = $("#filled_form_id").val();
//     // console.log(filledFormId);


//     $.post('/message',  formValues, messagePostComplete);
// // }

// function getStatus() {


//     // console.log("inside get status");

//     let filledFormId = $("#filled_form_id").val();

//     $.get("/app-status/" + filledFormId, showStatus);

}

$("#victim_direct_message").on("submit", postMessage);
// getStatus();

