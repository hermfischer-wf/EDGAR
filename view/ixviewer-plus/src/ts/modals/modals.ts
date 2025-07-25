/* Created by staff of the U.S. Securities and Exchange Commission.
 * Data and content created by government employees within the scope of their employment 
 * are not subject to domestic copyright protection. 17 U.S.C. 105.
 */

import { ConstantsFunctions } from "../constants/functions";
// import { FactMap } from "../facts/map";
import { ModalsCommon } from "./common";
import { ModalsFormInformation } from "./form-information";

export const Modals = {

	renderCarouselIndicators: (carouselId: string, indicatorId: string, carouselInformation: Array<{ 'dialog-title': string }>, currentSlide = 0) => {
		const elementToReturn = document.createDocumentFragment();
		if (currentSlide > 0) {
			currentSlide--;
		}
		carouselInformation.forEach((current, index) => {
			const activeSlide = (index === (currentSlide)) ? 'active' : '';

			const button = document.createElement('button');
			button.type = 'button';
			button.setAttribute('class', `${activeSlide} ix-focus`);
			button.setAttribute('data-bs-target', `#${carouselId}`);
			button.setAttribute('data-bs-slide-to', `${index}`);
			button.setAttribute('title', current['dialog-title']);
			button.setAttribute('tabindex', '16');

			elementToReturn.appendChild(button);
		});
		ConstantsFunctions.emptyHTMLByID(indicatorId);

		document.getElementById(indicatorId)?.appendChild(elementToReturn);
	},

	close: (event: Event | KeyboardEvent) => {

		if (Object.prototype.hasOwnProperty.call(event, 'key') && !((event as KeyboardEvent).key === 'Enter' 
		|| (event as KeyboardEvent).key === 'Space' || (event as KeyboardEvent).key === ' ')) {
			return;
		}
			
		document.getElementById('fact-copy-paste')?.classList.add('d-none');

		window.removeEventListener('keyup', ModalsFormInformation.keyboardEvents);
		window.removeEventListener('keyup', ModalsCommon.keyboardEvents);

		// to simplify things, we are going to go through and close every
		// dialog.
		const foundDialogs = document.querySelectorAll('.dialog-box');

		const foundDialogsArray = Array.prototype.slice.call(foundDialogs);

		foundDialogsArray.forEach((current) => {

			current.classList.remove('expand-modal');
			const viewPortWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
			if (viewPortWidth >= 576) {
				document.getElementById('fact-modal-expand')?.classList.remove('d-none');
				document.getElementById('fact-nested-modal-expand')?.classList.remove('d-none');

			}
			document.getElementById('fact-modal-compress')?.classList.add('d-none');
			document.getElementById('fact-nested-modal-compress')?.classList.add('d-none');

			current.classList.add('d-none');
		});
	},

	copyContent: (event: MouseEvent | KeyboardEvent, elementIdToCopy: string, copyPasteElement: string) => {
		
		if ("key" in event && !(event.key === "Enter" || event.key === "Space" || event.key === " " )) {
			return;
		}

		if (!document.getElementById(copyPasteElement)?.classList.contains('d-none')) {
			document.getElementById(copyPasteElement)?.classList.add('d-none');
		} else {
			const sectionToPopulate = '#' + copyPasteElement;
			document.getElementById(copyPasteElement)?.classList.remove('d-none');

			const foundCarouselPagesArray = Array.from(document.getElementById(elementIdToCopy)?.querySelectorAll('.carousel-item') || []);
			// TODO should we just put all of the innerText automatically into the user's clipboard?

			// th elements are the keys
			// td elements are the values
			let textToCopy = '';

			foundCarouselPagesArray.forEach((current) => {
				const foundInformation = current.querySelectorAll('table > * > tr');

				for(let nestedCurrent of foundInformation)
				{
					if (nestedCurrent.querySelector('th')?.innerText) {
						textToCopy += nestedCurrent.querySelector('th')!.innerText.trim() + ': ';
					}

					if (nestedCurrent.querySelector('td'))
					{
						const largeFactSelector = nestedCurrent.querySelector('td #collapse-modal');
						if (largeFactSelector instanceof HTMLElement)
						{
							textToCopy += '\n';
							textToCopy += largeFactSelector.innerText.trim().replace(/(\r\n|\n|\r)/gm, '');
							textToCopy += '\n';
						}
						else if (nestedCurrent.querySelector('td')?.innerText)
						{
							textToCopy += nestedCurrent.querySelector('td')!.innerText.trim().replace(/(\r\n|\n|\r)/gm, '');
							textToCopy += '\n';
						}
					}
				}
			});

			const textarea = document.querySelector(sectionToPopulate + " textarea");
			if (textarea != null)
			{
				textarea.textContent = textToCopy.trim();
			}
		}
	},

	closeCopy: (input: string) => {
		(document.getElementById(input) as HTMLElement).classList.add('d-none');
	},

	expandToggle: (
		event: MouseEvent | KeyboardEvent,
		idToTarget = 'fact-modal',
		idToExpand = 'fact-modal-expand',
		idToCompress = 'fact-modal-compress'
	) => {
		if (
			Object.prototype.hasOwnProperty.call(event, 'key') &&
			!((event as KeyboardEvent).key === 'Enter' ||
				(event as KeyboardEvent).key === 'Space' || (event as KeyboardEvent).key === ' ')
		) {
			return;
		}
		// idToTarget = idToTarget || 'fact-modal';
		// idToExpand = idToExpand || 'fact-modal-expand';
		// idToCompress = idToCompress || 'fact-modal-compress';

		const modalElement = document.getElementById(idToTarget);
		modalElement?.classList.toggle('expand-modal');
		if (modalElement?.classList.contains('expand-modal')) {

			document.getElementById(idToExpand)?.classList.add('d-none');
			document.getElementById(idToCompress)?.classList.remove('d-none');
			document.getElementById('fact-modal-drag')?.classList.add('d-none');
			document.getElementById(idToCompress)?.focus();

		} else {

			document.getElementById(idToExpand)?.classList.remove('d-none');
			document.getElementById(idToCompress)?.classList.add('d-none');
			document.getElementById('fact-modal-drag')?.classList.remove('d-none');
			document.getElementById(idToExpand)?.focus();
		}
	},

	initDrag: (element: HTMLElement) => {

		let factModal: {
			offsetLeft: number;
			clientWidth: number;
			offsetTop: number;
			clientHeight: number;
			style: { left: string; top: string; };
			offsetWidth: number;
			offsetHeight: number;
		} | null = null;
		let mouseXPos = 0;
		let mouseYPos = 0;
		let xElement = 0;
		let yElement = 0;

		const setStartDragState = (element: HTMLElement) => {
			factModal = element;
			xElement = (mouseXPos - factModal.offsetLeft) + (factModal.clientWidth / 2);
			yElement = (mouseYPos - factModal.offsetTop) + (factModal.clientHeight / 2);
		}

		// Define a flag to track if the function is enabled
		let isFunctionEnabled = false;

		const iconFactNestedModalDrag = document.getElementById('fact-nested-modal-drag');
		iconFactNestedModalDrag!.addEventListener("mouseover", () => {
			isFunctionEnabled = true; // Enable the function
			handleMouseOver(); // Call the function if needed
		});

		iconFactNestedModalDrag!.addEventListener('mouseout', () => {
			isFunctionEnabled = false; // Disable the function
		});

		const iconFactModalDrag = document.getElementById('fact-modal-drag');
		iconFactModalDrag!.addEventListener("mouseover", () => {
			isFunctionEnabled = true; // Enable the function
			handleMouseOver(); // Call the function if needed
		});

		iconFactModalDrag!.addEventListener('mouseout', () => {
			isFunctionEnabled = false; // Disable the function
		});

		element.onmousedown = function () {
			// not a fan of having all these .parentNode
			setStartDragState(this.parentNode.parentNode.parentNode);
			return false;
		};

		function handleMouseOver() {
			if (isFunctionEnabled) {
				// Will be called when user dragging an element
				const dragElement = (event: MouseEvent) => {
					mouseXPos = event.pageX;
					mouseYPos = event.pageY;

					if (factModal != null) {
						// drag freely while keeping drag button in the client window
						factModal.style.left = (mouseXPos >= 10 && mouseXPos <= window.innerWidth - 14) ? ((mouseXPos - xElement) + factModal.offsetWidth / 2) + 'px' : xElement.toString();
						factModal.style.top = (mouseYPos >= 60 && mouseYPos <= window.innerHeight - 14) ? ((mouseYPos - yElement) + factModal.offsetHeight / 2) + 'px' : yElement.toString();
					}
				}

				// Destroy the object when we are done
				const destroyDrag = () => {
					factModal = null;
					document.onmousemove = null;
				}

				document.onmousemove = dragElement;
				document.onmouseup = destroyDrag;
			}
		}

	}
};
