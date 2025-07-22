// register functions for when usertype selector is changed
window.onload = function() {

    document.getElementById('UserType').addEventListener("change", selectedTypeChanged);
    document.querySelectorAll('.changeTypeBtn').forEach( e => e.addEventListener("click", changeTypeBtnClicked));
}

function changeTypeBtnClicked(e) {

    userEmail = e.target.dataset.email;
    userType = e.target.dataset.userType;
    updateChangeTypeModal(userEmail, userType);
    $('#changeTypeModal').modal('show');
}

function updateChangeTypeModal(userEmail, userType) {
    document.getElementById('changeTypeModalEmailHiddenInput').value = userEmail;
    document.getElementById('changeTypeModalEmail').innerHTML = userEmail;

    currentUserTextElement = document.getElementById('changeTypeModalCurrentUserType');

    if (userType == 'admin') {
        currentUserTextElement.innerHTML = "Administrator";
        document.getElementById('changeTypeModalAdminOption').setAttribute('selected', '');
    }
    if (userType == 'coordinator') {
        currentUserTextElement.innerHTML = "Coordinator";
        document.getElementById('changeTypeModalCoordinatorOption').setAttribute('selected', '');
    }
    if (userType == 'facilitator') {
        currentUserTextElement.innerHTML = "Facilitator";
        document.getElementById('changeTypeModalFacilitatorOption').setAttribute('selected', '');
    }

    document.getElementById('changeTypeModalSelect').addEventListener('change', showWarning);
}

function showWarning(e) {

    newType = e.target.value;
    oldType = document.getElementById('changeTypeModalCurrentUserType').innerHTML;
    warningDivElement = document.getElementById('changeTypeModalWarningDiv');

    if (newType == 'facilitator' && (oldType == 'Administrator' || oldType == 'Coordinator')) {
        warningDivElement.style.display = "block";
    }
    else {
        warningDivElement.style.display = "none";
    }

}

function selectedTypeChanged(e) {

    selectedUserType = e.target.value;
    window.location.href = '/admin?selectedType=' + selectedUserType;
}