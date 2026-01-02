function editNames() {
	// change text to input
	
	const fnameElement = document.getElementById('first-name-div');
	const lnameElement = document.getElementById('last-name-div');

	fnameElement.classList.add('d-none');
	lnameElement.classList.add('d-none');

	const formElement = document.getElementById('edit-names-form');
	formElement.classList.remove('d-none');

	// change edit names button to save names button

	const editBtnElement = document.getElementById('edit-names-button');
	editBtnElement.classList.add('d-none');

}