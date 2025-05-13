function togglePassword() {
	const passwordField = document.querySelector('#id_password');
	const toggleIcon = document.querySelector('#toggleIcon');

	if (passwordField.type === 'password') {
		passwordField.type = 'text';
		toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
	} else {
		passwordField.type = 'password';
		toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
	}
}

document.addEventListener('DOMContentLoaded', () => {
	const passwordField = document.querySelector('#id_password');
	const toggleIcon = document.querySelector('#toggleIcon');

	if (passwordField && toggleIcon) {
		passwordField.type = 'password';
		toggleIcon.classList.add('fa-eye-slash');
	}
});
