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
                modalTextElement.innerHTML += "This student is currently signed into " + existingSessionName + ", which is currently running, and they haven't been signed out yet."

                $('#confirmTransferStudentModal').modal('show');
            }
            // if the student isn't already in a different class, just submit the form
            else if (data['result'] === "false" || data['result'] === "sign_out") {
                submitStudentSignInForm();
            }
            
            else if (data['result'] === "validateError") {
                
                // anything here??
            }
        },
        error: function(error) {
            console.error("Error signing student in", error);
        }
    });

	return false; // Ensure no unexpected behaviour
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