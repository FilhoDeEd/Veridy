const searchForm = document.getElementById('search-form');

if (searchForm) {
	const dropdownItems = searchForm.querySelectorAll('.dropdown-item');
	const targetInput = searchForm.querySelector('#search-target');
	const dropdownIcon = searchForm.querySelector('#search-icon');

	const savedTarget = localStorage.getItem('searchTarget');
	const savedIcon = localStorage.getItem('searchIcon');
	if (savedTarget && savedIcon) {
		targetInput.value = savedTarget;
		dropdownIcon.className = `fas ${savedIcon} theme-inverse`;
	}

	dropdownItems.forEach((item) => {
		item.addEventListener('click', function (e) {
			e.preventDefault();
			const target = this.dataset.target;
			const icon = this.dataset.icon;

			targetInput.value = target;
			dropdownIcon.className = `fas ${icon} theme-inverse`;

			localStorage.setItem('searchTarget', target);
			localStorage.setItem('searchIcon', icon);
		});
	});

	searchForm.addEventListener('submit', function (e) {
		e.preventDefault();
		const query = this.querySelector('input[name="q"]').value;
		const target = this.querySelector('input[name="target"]').value;

		const urlInput = document.getElementById(`url-${target}`);
		const url = urlInput?.value || '/';

		window.location.href = `${url}?q=${encodeURIComponent(query)}`;
	});
}
