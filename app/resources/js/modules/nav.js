export default class Navigation {
	constructor(options) {
		this.maxHeight = undefined;
		this.el = options.element;

		let self = this;

		if (this.el.getAttribute('data-set-max-height')) {
			this.el.style.maxHeight = 0;

			const observer = new MutationObserver(function () {
				self.update();
			});

			observer.observe(self.el, {
				attributes: true,
				attributeFilter: ['class'],
				childList: false,
				characterData: false
			});
		}
	}

	getHeight() {
		let h;
		let maxHeight = this.el.style.maxHeight;

		this.el.style.maxHeight = 'none';
		h = this.el.offsetHeight;
		this.el.style.maxHeight = maxHeight;

		return h;
	}

	update() {
		const self = this;
		if (this.el.classList.contains('is-visible')) {
			if (this.maxHeight === undefined) {
				this.maxHeight = this.getHeight();
			}

			//wihtout setTimeout style change won't be animated
			setTimeout(function() {
				self.el.style.maxHeight = self.maxHeight + 'px';
			}, 0);
		} else {
			this.el.style.maxHeight = 0;
		}
	}
}
