/**
 * Reusable Navbar Component
 * Injects the navigation bar into the #navbar-container element
 */
document.addEventListener("DOMContentLoaded", function () {
    const navbarContainer = document.getElementById("navbar-container");
    if (!navbarContainer) return;

    navbarContainer.innerHTML = `
        <nav class="navbar premium-navbar">
            <div class="container nav-flex">
                <a href="dashboard.html" class="logo-text">
                    <span class="logo-badge"><i class="fas fa-robot"></i></span>
                    <span>CareerAI</span>
                </a>

                <div class="nav-links" id="mainNavLinks">
                    <a href="dashboard.html" class="nav-item">Home</a>
                    <a href="career_preference.html" class="nav-item">Career Preference</a>

                    <div class="dropdown" id="collegeDropdown">
                        <button class="dropbtn nav-item" type="button" aria-expanded="false">
                            <span>Colleges</span>
                            <i class="fas fa-chevron-down"></i>
                        </button>
                        <div class="dropdown-content">
                            <a href="colleges_engineering.html">Engineering (CET/JEE)</a>
                            <a href="colleges_medical.html">Medical (NEET)</a>
                            <a href="colleges_high_school.html">11th/12th (FYJC)</a>
                            <a href="after_graduation.html">After Graduation</a>
                        </div>
                    </div>
                </div>

                <div class="nav-auth" id="authNav">
                    <a href="login.html" class="btn-login">
                        <i class="fas fa-sign-in-alt"></i>
                        <span>Login</span>
                    </a>
                </div>

                <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Toggle navigation" type="button">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
        </nav>
    `;

    const currentPath = window.location.pathname.split("/").pop() || "dashboard.html";
    const navLinks = navbarContainer.querySelectorAll(".nav-links a, .logo-text, .dropdown-content a");

    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href === currentPath) {
            link.classList.add("active");

            const parentDropdown = link.closest(".dropdown");
            if (parentDropdown) {
                const dropBtn = parentDropdown.querySelector(".dropbtn");
                if (dropBtn) dropBtn.classList.add("active");
            }
        }
    });

    const mobileBtn = navbarContainer.querySelector("#mobileMenuBtn");
    const navLinksWrapper = navbarContainer.querySelector("#mainNavLinks");
    const dropdown = navbarContainer.querySelector("#collegeDropdown");
    const dropdownBtn = navbarContainer.querySelector(".dropbtn");

    if (mobileBtn && navLinksWrapper) {
        mobileBtn.addEventListener("click", () => {
            navLinksWrapper.classList.toggle("active");

            const icon = mobileBtn.querySelector("i");
            if (navLinksWrapper.classList.contains("active")) {
                icon.classList.remove("fa-bars");
                icon.classList.add("fa-xmark");
            } else {
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            }
        });
    }

    if (dropdownBtn && dropdown) {
        dropdownBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            const isOpen = dropdown.classList.toggle("open");
            dropdownBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
        });
    }

    document.addEventListener("click", function (e) {
        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.classList.remove("open");
            if (dropdownBtn) dropdownBtn.setAttribute("aria-expanded", "false");
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 980) {
            navLinksWrapper.classList.remove("active");
            if (mobileBtn) {
                const icon = mobileBtn.querySelector("i");
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            }
        }
    });
});