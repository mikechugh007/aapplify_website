
const toggleButton = document.getElementById("toggleButton");
if (toggleButton) {
  toggleButton.addEventListener("click", function () {
    const openIcon = document.getElementById("openIcon");
    const closeIcon = document.getElementById("closeIcon");
    const mobileMenu = document.getElementById("mobileMenu");

    if (!openIcon || !closeIcon || !mobileMenu) return;

    if (openIcon.classList.contains("hidden")) {
      openIcon.classList.remove("hidden");
      closeIcon.classList.add("hidden");
      mobileMenu.classList.add("translate-x-96");
      mobileMenu.classList.remove("translate-x-0");
    } else {
      openIcon.classList.add("hidden");
      closeIcon.classList.remove("hidden");
      mobileMenu.classList.add("translate-x-0");
      mobileMenu.classList.remove("translate-x-96");
    }
  });
}

function closeMobileMenu() {
    const mobileMenu = document.getElementById("mobileMenu");
    const openIcon = document.getElementById("openIcon");
    const closeIcon = document.getElementById("closeIcon");

    if (!mobileMenu || !openIcon || !closeIcon) return;

    mobileMenu.classList.add("translate-x-96");
    mobileMenu.classList.remove("translate-x-0");
    openIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
}

const closeSide = document.getElementById("closeSide");
if (closeSide) closeSide.addEventListener("click", closeMobileMenu);
document.querySelectorAll(".mobile_menu_list").forEach(function(element) {
    element.addEventListener("click", closeMobileMenu);
});


// Get the button and menu elements
const menuButton = document.getElementById('menu-button');
const menu = document.querySelector('[role="menu"]');

if (menuButton && menu) {
  // Toggle the menu visibility
  menuButton.addEventListener('click', function () {
    const isMenuOpen = menu.getAttribute('aria-expanded') === 'true';

    // Toggle the aria-expanded attribute
    menu.setAttribute('aria-expanded', !isMenuOpen);

    // Toggle the menu visibility
    if (isMenuOpen) {
      menu.classList.add('hidden'); // Hide the menu
    } else {
      menu.classList.remove('hidden'); // Show the menu
    }
  });

  // Hide the menu when clicking outside
  document.addEventListener('click', function (event) {
    const isClickInside = menuButton.contains(event.target) || menu.contains(event.target);

    if (!isClickInside) {
      menu.classList.add('hidden');
      menu.setAttribute('aria-expanded', 'false');
    }
  });
}
