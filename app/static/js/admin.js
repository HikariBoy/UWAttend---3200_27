// register functions for when usertype selector is changed
window.onload = function() {

    document.getElementById('UserType').addEventListener("change", selectedTypeChanged);
    document.querySelectorAll('.changeTypeBtn').forEach( e => e.addEventListener("click", changeTypeBtnClicked));
}

function changeTypeBtnClicked(e) {

    userEmail = e.target.dataset.email;
    userType = e.target.dataset.userType;
    $('#changeTypeModal').modal('show');
}

function selectedTypeChanged(e) {

    selectedUserType = e.target.value;
    window.location.href = '/admin?selectedType=' + selectedUserType;
}

function changeType() {
    alert('changing type...');
}