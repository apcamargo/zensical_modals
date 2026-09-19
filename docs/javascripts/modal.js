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

const openers = new WeakMap();

function openDialog(dialog, opener) {
  openers.set(dialog, opener);
  if (!dialog.open) dialog.showModal();
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

function prepareTrigger(trigger, dialog) {
  trigger.classList.add("modal-trigger");
  trigger.setAttribute("role", "button");
  trigger.setAttribute("tabindex", "0");
  trigger.setAttribute("aria-haspopup", "dialog");

  trigger.addEventListener("click", () => openDialog(dialog, trigger));
  trigger.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    openDialog(dialog, trigger);
  });
}

document$.subscribe(({ body }) => {
  measureContentWidth();

  const dialogsByKey = new Map();

  for (const dialog of body.querySelectorAll(".modal[modal]")) {
    dialogsByKey.set(dialog.getAttribute("modal"), dialog);
    dialog.addEventListener("close", () => {
      openers.get(dialog)?.focus({ preventScroll: true });
    });
    dialog.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeDialog(dialog);
    });
  }

  for (const trigger of body.querySelectorAll("span[modal]")) {
    const dialog = dialogsByKey.get(trigger.getAttribute("modal"));
    if (dialog) prepareTrigger(trigger, dialog);
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
