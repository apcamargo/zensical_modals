/* The modals are as wide as the page's content column. The variable is
   published once on the document root and consumed by the modal styles. */
function measureContentWidth() {
  const content = document.querySelector(".md-content__inner");
  if (!(content instanceof HTMLElement)) return;
  document.documentElement.style.setProperty(
    "--modal-width",
    `${Math.round(content.getBoundingClientRect().width)}px`,
  );
}

let resizeFrame = 0;
window.addEventListener("resize", () => {
  cancelAnimationFrame(resizeFrame);
  resizeFrame = requestAnimationFrame(measureContentWidth);
});

// Web fonts load after the first measure and can reflow the content column.
document.fonts.ready.then(measureContentWidth);

const CLOSING_CLASS = "modal--closing";

function openDialog(dialog) {
  dialog.showModal();
}

async function closeDialog(dialog) {
  if (dialog.classList.contains(CLOSING_CLASS)) return;
  dialog.classList.add(CLOSING_CLASS);

  const animations = dialog.getAnimations({ subtree: true });
  await Promise.allSettled(animations.map((animation) => animation.finished));
  await new Promise(requestAnimationFrame);

  dialog.classList.remove(CLOSING_CLASS);
  dialog.close();
}

document$.subscribe(({ body }) => {
  measureContentWidth();

  for (const trigger of body.querySelectorAll("[data-modal]")) {
    const dialogId = trigger.dataset.modal;
    const dialog = dialogId ? body.querySelector(`#${dialogId}`) : null;

    if (!(dialog instanceof HTMLDialogElement)) continue;

    trigger.addEventListener("click", () => openDialog(dialog));
    dialog.addEventListener("close", () => trigger.focus({ preventScroll: true }));
    dialog.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeDialog(dialog);
    });
  }

  for (const closeButton of body.querySelectorAll("[data-modal-close]")) {
    const dialog = closeButton.closest("dialog");
    if (dialog) closeButton.addEventListener("click", () => closeDialog(dialog));
  }

  for (const dialog of body.querySelectorAll(".modal")) {
    dialog.addEventListener("click", (event) => {
      if (event.target.closest(".modal__surface") === null) closeDialog(dialog);
    });
  }
});
