// register functions for when usertype selector is changed
window.onload = function() {
    document.getElementById('UserType').addEventListener("change", userTypeChanged);
    hideOrShowEmailAndSubmitContainer(document.getElementById('UserType').value);
    changeHeadings(document.getElementById('UserType').value);
}

function userTypeChanged(e) {

    selectedUserType = e.target.value;
    changeHeadings(selectedUserType);
    hideOrShowEmailAndSubmitContainer(selectedUserType);
    removeErrors();
}

function hideOrShowEmailAndSubmitContainer(selectedUserType) {
    let containerElement = document.getElementById("emailAndSubmitContainer");
    
    if (selectedUserType == "facilitator") {
        containerElement.style.display = "none";
    }
    else {
        containerElement.style.display = "block";
    }
}

function removeErrors() {
    const errorElements = document.querySelectorAll('.addUserFormError');
    errorElements.forEach( e => e.remove());
}

function changeHeadings(selectedUserType) {
    const headingSpanElements = document.querySelectorAll('.userTypeValue');

    for (let span of headingSpanElements) {
        if (selectedUserType == "admin") {
            span.innerHTML = "Admin";
        }
        if (selectedUserType == "coordinator") {
            span.innerHTML = "Coordinator";
        }
        if (selectedUserType == "facilitator") {
            span.innerHTML = "Facilitator";
        }
    }
}