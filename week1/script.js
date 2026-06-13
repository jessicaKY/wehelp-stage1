const burgerButton = document.querySelector(".burger-button");
const closeButton = document.querySelector(".close-button");
const mobileMenu = document.querySelector(".mobile-menu");
const menuBackdrop = document.querySelector(".menu-backdrop");

function openMenu() {
  mobileMenu.classList.add("open");
  mobileMenu.setAttribute("aria-hidden", "false");
  burgerButton.setAttribute("aria-expanded", "true");
  menuBackdrop.hidden = false;
}

function closeMenu() {
  mobileMenu.classList.remove("open");
  mobileMenu.setAttribute("aria-hidden", "true");
  burgerButton.setAttribute("aria-expanded", "false");
  menuBackdrop.hidden = true;
}

burgerButton.addEventListener("click", openMenu);
closeButton.addEventListener("click", closeMenu);
menuBackdrop.addEventListener("click", closeMenu);

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeMenu();
  }
});
