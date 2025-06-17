$("#student_sign_in_button").click(function (e) {
	e.preventDefault();  // Prevent the default form submission
    checkStudentInOtherSession();

});

function checkStudentInOtherSession() {

    $.ajax({
        type: "POST",
        url: "/checkstudentinothersession",
        data: $('#attendanceForm').serialize(),    // serialise the form's contents
        datatype: 'json',
        success: function(data) {

            // if the student is already in a session and hasn't been signed out
            if (data['result'] === "true") {

                const existingSessionName = data['existingSessionName'];

                let modalTextElement = $("#confirmTransferStudentModalExistingSessionText").get(0);
                modalTextElement.innerHTML = "This student is signed into <b>" + existingSessionName + "</b>, which is currently running, and they haven't been signed out yet."

                $('#confirmTransferStudentModal').modal('show');
            }
            // if the student isn't already in a different class, just submit the form

            else if (data['result'] === "sign_out") {
                addAttendance();
            }
            else if (data['result'] === "false") {
                checkConsent();
            }
            
            else if (data['result'] === "validateError") {
                
                // anything here??
            }
            else if (data['result'] === "session_not_found") {
                // if the session ID (in the cookie) was not valid
                // add a flash message??
            }
        },
        error: function(error) {
            console.error("Error signing student in", error);
        }
    });

	return false; // Ensure no unexpected behaviour
}

function checkConsent() {

	$('#confirmTransferStudentModal').modal('hide');

	// Only display the modal if consent has not been previously granted 
	if ($("#hidden_consent_indicator").val() == "yes") {
		$("#consentModal").modal('show');
		document.getElementById('hidden_consent_indicator').value = "no";
	} else {
		addAttendance();
	}
	return false;
}

function submitStudentSignInForm() {

    

    $.ajax({
        type: "POST",
        url: '/add_student',
        data: $('#attendanceForm').serialize(),    // serialise the forms contents
        success: function() {
            window.location.href = '/home';  // Redirect to home after successfully configuring/updating session
        },
        error: function(error) {
            console.error("Error configuring/updating session", error);
        }
    });

	return false; // Ensure no unexpected behaviour

}

//Calls an ajax function to a backend route, passing the consent in JSON format
function addAttendance(consent = "none") {

	// Set the consent value in the hidden field
    $("#consent_status").val(consent);

    // Log the consent for testing
    console.log("Consent was given: " + consent);

    // Close the modal before submitting
    $("#consentModal").modal('hide');

	console.log("Final Consent Status: " + $("#consent_status").val());

    // Submit the form after setting the consent status
    $("#attendanceForm").off("submit").submit();  // Ensure the form is submitted this time

	return false; // Ensure no unexpected behaviour
}