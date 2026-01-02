function editNames() {
	// change text to input
	
	const fnameElement = document.getElementById('first-name-div');
	const lnameElement = document.getElementById('last-name-div');

	let fname = fnameElement.innerText;
	let lname = lnameElement.innerText;

	fnameElement.innerText = "";
	lnameElement.innerText = "";

	fnameElement.appendChild(getNameInputElement(fname));
	lnameElement.appendChild(getNameInputElement(lname));

	// change edit names button to save names button

	const editBtnElement = document.getElementById('edit-names-button');
	editBtnElement.classList.add('d-none');

	const saveBtnElement = document.getElementById('save-names-button');
	saveBtnElement.classList.remove('d-none');
}

function getNameInputElement(name) {
	const nameInput = document.createElement('input');
	nameInput.classList.add('form-control');
	nameInput.setAttribute('value', name);
	return nameInput;
}

function saveNames() {
	alert('saved');
}