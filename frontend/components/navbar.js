/**
 * Reusable Navbar Component matching dashboard style
 * Injects the navigation bar into the #navbar-container element
 */
document.addEventListener("DOMContentLoaded", function () {
    const navbarContainer = document.getElementById("navbar-container");
    if (!navbarContainer) return;

    navbarContainer.innerHTML = `
        <div class="nav-fixed-layout">
            <a href="dashboard.html" class="nav-brand">
                <i class="fas fa-briefcase"></i>
                CareerAI
            </a>
            <div class="nav-right">
                <a href="dashboard.html" class="nav-link">Home</a>
                <a href="career_preference.html" class="nav-link">Career Preference</a>
                <a href="colleges_engineering.html" class="nav-link">Engineering</a>
                <a href="colleges_medical.html" class="nav-link">Medical</a>
                <a href="colleges_high_school.html" class="nav-link">11th/12th</a>
                <a href="after_graduation.html" class="nav-link">After Graduation</a>
                <div class="nav-user">
                    <a href="login.html">Login</a>
                </div>
            </div>
        </div>
    `;

    // Set active link based on current page
    const currentPath = window.location.pathname.split("/").pop() || "dashboard.html";
    const navLinks = navbarContainer.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href === currentPath) {
            link.classList.add("active");
        }
    });

    // Theme toggle (if present)
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const html = document.documentElement;
            const isDark = html.getAttribute('data-theme') === 'dark';
            html.setAttribute('data-theme', isDark ? 'light' : 'dark');
            this.innerHTML = isDark
                ? '<i class="fas fa-moon"></i>'
                : '<i class="fas fa-sun"></i>';
        });
    }
});