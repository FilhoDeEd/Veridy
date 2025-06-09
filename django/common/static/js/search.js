const searchForm = document.getElementById('search-form');

if (searchForm) {
	const dropdownItems = searchForm.querySelectorAll('.dropdown-item');
	const targetInput = searchForm.querySelector('#search-target');
	const dropdownLabel = searchForm.querySelector('#search-dropdown span');

	dropdownItems.forEach((item) => {
		item.addEventListener('click', function (e) {
			e.preventDefault();
			const target = this.dataset.target;
			targetInput.value = target;
			dropdownLabel.innerText = this.innerText;
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
