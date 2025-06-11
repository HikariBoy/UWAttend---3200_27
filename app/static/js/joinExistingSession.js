//When submit button for session config form is clicked
$("#submit").click(function (e) {
	e.preventDefault();  // Prevent the default form submission

    const form = document.getElementById("sessionForm");
    let updateStatus = form.getAttribute("data-update");
    console.log(updateStatus);
    if (updateStatus === 'true') {
        confirmSessionEdits();
    }
    else {
        checkSessionExists();
    }
});

function confirmSessionEdits() {
    let modalTextElement = $("#confirmSessionEditsModalChangesText").get(0);

    //retrieve current session details
    const currentSessionName = $("#currentSessionName").get(0).innerHTML;
    const currentSessionTime = $("#currentSessionTime").get(0).innerHTML;
    const currentSessionDate = $("#currentSessionDate").get(0).innerHTML;

    //retrieve new session details
    const newSessionName = $("#session_name").get(0).value;
    const newSessionTime = $("#session_time").get(0).value;
    const newSessionDate = $("#session_date").get(0).value;

    modalTextElement.innerHTML = "";
    let changesMade = false;

    if (currentSessionName != newSessionName) {
        modalTextElement.innerHTML += "<br>" + currentSessionName + " > " + newSessionName;
        changesMade = true;
    }
    if (currentSessionTime != newSessionTime) {
        modalTextElement.innerHTML += "<br>" + currentSessionTime + " > " + newSessionTime;
        changesMade = true;

    }
    if (currentSessionDate != newSessionDate) {
        modalTextElement.innerHTML += "<br>" + currentSessionDate + " > " + newSessionDate;
        changesMade = true;
    }

    if (changesMade) {
        $('#confirmSessionEditsModal').modal('show');
    }


}

function confirmChanges() {
    $('#confirmSessionEditsModal').modal('hide');
    checkSessionExists();
}

function checkSessionExists() {

    $.ajax({
        type: "POST",
        url: "/checksessionexists",
        data: $('form').serialize(),    // serialise the form's contents
        datatype: 'json',
        success: function(data) {
            // if the session already exists, show the warning modal
            if (data['result'] === "true") {

                const facilitatorNamesLength = data['facilitatorNames'].length;

                // if the session exists, but there are no students, immediately configure session
                if (facilitatorNamesLength == 0) {
                    submitSessionForm();
                }
                // if the session exists and has students signed in, say which facilitators have signed them in
                else {
                    let modalTextElement = $("#joinExistingSessionModalText").get(0);
                    modalTextElement.innerHTML = "You are joining an existing session with students signed in by: ";
                    for (let i = 0; i < facilitatorNamesLength; i++) {
                        modalTextElement.innerHTML += data['facilitatorNames'][i];
                        if (i != facilitatorNamesLength - 1) {
                            modalTextElement.innerHTML += ', ';
                        }
                    }
                    $('#joinExistingSessionModal').modal('show');
                }
            }
            // if the session doesn't exist, immediately configure session
            else if (data['result'] === "false") {
                submitSessionForm();
            }
            
            else if (data['result'] === "validateError") {
                
                const errorSpan = $("#errorMsg").get(0);
                errorSpan.innerHTML = "Please select a valid option for all fields."
                errorSpan.classList.remove("invisible");
            }
        },
        error: function(error) {
            console.error("Error configuring/updating session", error);
        }
    });

	return false; // Ensure no unexpected behaviour
}

function submitSessionForm() {

    // hide the modal (if there is one)
    $('#joinExistingSessionModal').modal('hide');

    // set route appropriately depending on whether form is to update or not
    let route = '';
    let update = $('form').attr('data-update');
    if (update == "true") {
        route = "/updatesession";
    }
    else {
        route = "/session";
    }

    $.ajax({
        type: "POST",
        url: route,
        data: $('form').serialize(),    // serialise the forms contents
        success: function() {
            window.location.href = '/home';  // Redirect to home after successfully configuring/updating session
        },
        error: function(error) {
            console.error("Error configuring/updating session", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}