// ===============================
// FreshMart Main JavaScript File
// ===============================

// ========== THEME TOGGLE ==========
const themeToggle = document.getElementById("theme-toggle");
if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    const icon = themeToggle.querySelector("i");
    if (document.body.classList.contains("dark-theme")) {
      icon.classList.replace("fa-sun", "fa-moon");
      localStorage.setItem("theme", "dark");
    } else {
      icon.classList.replace("fa-moon", "fa-sun");
      localStorage.setItem("theme", "light");
    }
  });

  // Apply saved theme on load
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
    const icon = themeToggle.querySelector("i");
    if (icon) icon.classList.replace("fa-sun", "fa-moon");
  }
}

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