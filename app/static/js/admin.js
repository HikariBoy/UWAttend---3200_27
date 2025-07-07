// register functions for when usertype selector is changed
window.onload = function() {
    document.getElementById('UserType').addEventListener("change", userTypeChanged);
}

function userTypeChanged(e) {

    selectedUserType = e.target.value;
    disableOrEnableAddUserBtn(selectedUserType);

}

function disableOrEnableAddUserBtn(selectedUserType) {
    let btnElement = document.getElementById("submit");
    
    if (selectedUserType == "facilitator") {
        btnElement.setAttribute("disabled", "");
    }
    else {
        btnElement.removeAttribute("disabled");
    }
}