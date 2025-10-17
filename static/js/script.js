// ===============================
// FreshMart Main JavaScript File
// ===============================

// ========== THEME TOGGLE ==========
document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.querySelector(".theme-toggle-btn");
  if (!themeToggle) return;

  const body = document.body;
  const sunIcon = themeToggle.querySelector(".fa-sun");
  const moonIcon = themeToggle.querySelector(".fa-moon");

  // Load saved theme
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    body.classList.add("dark-mode");
    sunIcon.style.display = "none";
    moonIcon.style.display = "inline";
  } else {
    sunIcon.style.display = "inline";
    moonIcon.style.display = "none";
  }

  // Toggle theme on click
  themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    const darkMode = body.classList.contains("dark-mode");

    if (darkMode) {
      sunIcon.style.display = "none";
      moonIcon.style.display = "inline";
      localStorage.setItem("theme", "dark");
    } else {
      sunIcon.style.display = "inline";
      moonIcon.style.display = "none";
      localStorage.setItem("theme", "light");
    }
  });
});

// ========== SCROLL TO TOP ==========
const scrollTopBtn = document.getElementById("scroll-top-btn");
if (scrollTopBtn) {
  window.addEventListener("scroll", () => {
    scrollTopBtn.style.display = window.scrollY > 300 ? "block" : "none";
  });

  scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// ========== MOBILE MENU ==========
const menuToggle = document.querySelector(".menu-toggle");
const navMenu = document.querySelector(".nav-menu");

if (menuToggle && navMenu) {
  menuToggle.addEventListener("click", () => {
    navMenu.classList.toggle("active");
  });
}

// ========== PROMO BANNER CLOSE ==========
const promoClose = document.querySelector(".promo-close");
const promoBanner = document.querySelector(".promo-banner");

if (promoClose && promoBanner) {
  promoClose.addEventListener("click", () => {
    promoBanner.style.display = "none";
  });
}

// ========== SIMPLE UI ANIMATIONS ==========
document.addEventListener("DOMContentLoaded", () => {
  const fadeElements = document.querySelectorAll(".fade-in");
  fadeElements.forEach((el, index) => {
    setTimeout(() => {
      el.classList.add("visible");
    }, index * 150);
  });
});

// ========== NOTE: Cart actions now handled by Django backend ==========
/*
In your templates, your Add to Cart buttons should use:
<a href="{% url 'cart:add_to_cart' product.id %}" class="btn btn-primary">Add to Cart</a>

No JS cart needed — Django stores it in the session automatically.
*/