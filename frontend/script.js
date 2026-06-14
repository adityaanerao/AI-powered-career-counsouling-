/* ===============================
   Auto-detect state and initialize
   =============================== */
document.addEventListener('DOMContentLoaded', function () {
    // Set default values
    const stateInput = document.getElementById("state");
    if (stateInput) {
        stateInput.value = "Maharashtra";
    }

    // Add animation to form cards on load
    const formCards = document.querySelectorAll('.form-card');
    formCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add input validation
    setupInputValidation();

    // Check Auth State for Header
    updateAuthHeader();
});

/* ===============================
   Auth Functions
   =============================== */
function updateAuthHeader() {
    const nav = document.getElementById('authNav');
    if (!nav) return;

    const user = JSON.parse(localStorage.getItem('user'));

    if (user) {
        nav.innerHTML = `
            <span style="color: white; margin-right: 15px; font-weight: 500;">Hello, ${user.full_name.split(' ')[0]}</span>
            <a href="profile.html" class="btn-profile"><i class="fas fa-user-circle"></i> My Profile</a>
        `;
    } else {
        nav.innerHTML = `
            <a href="login.html" class="btn-login"><i class="fas fa-sign-in-alt"></i> Login</a>
            <a href="register.html" class="btn-register"><i class="fas fa-user-plus"></i> Get Started</a>
        `;
    }
}

function checkLoginState() {
    return localStorage.getItem('user') !== null;
}

async function registerUser() {
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!fullName || !email || !password) {
        alert("Please fill all fields");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: fullName, email, password })
        });

        const data = await response.json();
        if (response.ok) {
            // Auto login
            localStorage.setItem('user', JSON.stringify({ user_id: data.user_id, full_name: data.name, email: email }));
            window.location.href = 'dashboard.html';
        } else {
            alert(data.error || "Registration failed");
        }
    } catch (e) {
        console.error(e);
        alert("Server error");
    }
}

async function loginUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("Please fill all fields");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = 'dashboard.html';
        } else {
            alert(data.error || "Login failed");
        }
    } catch (e) {
        console.error(e);
        alert("Server error");
    }
}

function logoutUser() {
    localStorage.removeItem('user');
    window.location.href = 'dashboard.html';
}

/* ===============================
   Setup input validation
   =============================== */
function setupInputValidation() {
    // Add validation for CET percentile input
    const cetInput = document.getElementById('cet-percentile');
    if (cetInput) {
        cetInput.addEventListener('input', function () {
            const value = parseFloat(this.value);
            if (value < 0 || value > 100) {
                this.style.borderColor = '#e74c3c';
                showNotification("CET percentile must be between 0 and 100", "warning");
            } else {
                this.style.borderColor = '#e0e0e0';
            }
        });
    }
}

/* ===============================
   Update Form Based on Exam Type
   =============================== */
function updateFormForExamType() {
    const examSelect = document.getElementById("exam");
    if (!examSelect) return;

    const examType = examSelect.value;
    const percentileText = document.getElementById("percentile-text");
    const branchSelect = document.getElementById("branch");
    const universitySelect = document.getElementById("university");

    // Update Label
    if (percentileText) {
        if (examType === "SSC") {
            percentileText.textContent = "10th Percentage";
        } else if (examType === "HSC") {
            percentileText.textContent = "12th Percentage";
        } else if (["CAT", "GATE", "MCA-CET", "CET-PG"].includes(examType)) {
            percentileText.textContent = "Exam Score/Percentile";
        } else {
            percentileText.textContent = `${examType} Percentile`;
        }
    }

    // Update Branches
    if (branchSelect) {
        branchSelect.innerHTML = "";
        let options = [];

        if (examType === "NEET") {
            options = [
                { value: "MBBS", label: "MBBS" },
                { value: "BDS", label: "BDS (Dental)" },
                { value: "BAMS", label: "BAMS (Ayurveda)" },
                { value: "BHMS", label: "BHMS (Homeopathy)" },
                { value: "B.Pharm", label: "B.Pharm" }
            ];
            if (universitySelect && universitySelect.parentElement) {
                universitySelect.parentElement.style.display = 'none';
            }
        } else if (examType === "SSC" || examType === "HSC") {
            // Junior College
            options = [
                { value: "Science", label: "Science Stream" },
                { value: "Commerce", label: "Commerce Stream" },
                { value: "Arts", label: "Arts Stream" }
            ];
            if (universitySelect && universitySelect.parentElement) {
                universitySelect.parentElement.style.display = 'none';
            }
        } else if (["CAT", "GATE", "MCA-CET", "CET-PG"].includes(examType)) {
            // PG Courses
            if (examType === "GATE") {
                options = [{ value: "M.Tech CSE", label: "M.Tech CSE" }];
            } else if (examType === "CAT" || examType === "CET-PG") {
                options = [{ value: "MBA", label: "MBA" }];
            } else if (examType === "MCA-CET") {
                options = [{ value: "MCA", label: "MCA" }];
            }
            if (universitySelect && universitySelect.parentElement) {
                universitySelect.parentElement.style.display = 'block';
            }
        } else {
            // CET / JEE
            options = [
                { value: "Computer Engineering", label: "Computer Engineering" },
                { value: "Information Technology", label: "Information Technology" },
                { value: "Artificial Intelligence & Data Science", label: "AI & Data Science" },
                { value: "Artificial Intelligence & Machine Learning", label: "AI & ML" },
                { value: "Data Science", label: "Data Science" },
                { value: "Mechanical Engineering", label: "Mechanical Engineering" },
                { value: "Civil Engineering", label: "Civil Engineering" },
                { value: "Electrical Engineering", label: "Electrical Engineering" },
                { value: "Electronics & Telecommunication Engineering", label: "ENTC" }
            ];
            if (universitySelect && universitySelect.parentElement) {
                universitySelect.parentElement.style.display = 'block';
            }
        }

        options.forEach(opt => {
            const option = document.createElement("option");
            option.value = opt.value;
            option.textContent = opt.label;
            branchSelect.appendChild(option);
        });
    }
}

// Initialize form on load
document.addEventListener('DOMContentLoaded', function () {
    const examSelect = document.getElementById('exam');
    if (examSelect) {
        examSelect.addEventListener('change', updateFormForExamType);
        updateFormForExamType();
    }
});


/* ===============================
   Career Recommendation (AI)
   =============================== */
async function getRecommendations() {
    const interests = document.getElementById("interests").value;
    const skills = document.getElementById("skills").value;
    const subjects = document.getElementById("subjects").value;
    const cet = document.getElementById("cet").value || 0;

    // Validate inputs
    if (!interests && !skills && !subjects) {
        showNotification("Please fill in at least one field to get career recommendations.", "warning");
        return;
    }

    // Show loading state
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = `
        <div class="placeholder-message">
            <i class="fas fa-spinner fa-spin"></i>
            <p>AI is analyzing your profile to generate personalized career recommendations...</p>
        </div>
    `;

    try {
        const response = await fetch("http://127.0.0.1:5000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                interests,
                skills,
                subjects,
                cet_percentile: cet
            })
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();
        displayCareerResults(data);

    } catch (error) {
        console.error("Error fetching career recommendations:", error);
        showNotification("Unable to connect to the server. Showing demo data instead.", "warning");

        // Show demo data for UI demonstration
        showDemoCareerData();
    }
}

/* ===============================
   Display Career Results
   =============================== */
function displayCareerResults(data) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!data.recommendations || data.recommendations.length === 0) {
        resultsDiv.innerHTML = `
            <div class="placeholder-message">
                <i class="fas fa-search"></i>
                <p>No career recommendations found. Try adjusting your inputs for better results.</p>
            </div>
        `;
        return;
    }

    data.recommendations.forEach((rec, index) => {
        let explanationHTML = "<ul class='explanation-list'>";
        rec.explanation.forEach(reason => {
            explanationHTML += `<li>${reason}</li>`;
        });
        explanationHTML += "</ul>";

        // Determine icon based on category/career
        let icon = "💼";
        if (rec.category === "Technical") icon = "💻";
        if (rec.category === "Medical") icon = "⚕️";
        if (rec.category === "Arts") icon = "🎨";
        if (rec.category === "Business") icon = "📊";
        if (rec.category === "Government") icon = "🏛️";

        // Trending Badge
        let trendingBadge = "";
        if (rec.outlook && (rec.outlook.includes("High") || rec.outlook.includes("Growth"))) {
            trendingBadge = `<span class="badge badge-trending">🔥 ${rec.outlook}</span>`;
        }

        const card = document.createElement("div");
        card.className = "career-card expanded-card";
        card.style.animationDelay = `${index * 0.1}s`;

        card.innerHTML = `
            <div class="card-header">
                <h3>${icon} ${rec.career}</h3>
                ${trendingBadge}
            </div>

            <p class="career-desc">${rec.description}</p>

            <div class="score-bar">
                <strong>Match Score:</strong>
                <div class="bar-container">
                    <div class="bar-fill" style="width: ${rec.match_percentage}%"></div>
                    <span class="score-text">${rec.match_percentage}%</span>
                </div>
            </div>

            <div class="career-details-grid">
                <div class="detail-box">
                    <strong>💰 Avg Salary</strong>
                    <span>${rec.salary || "N/A"}</span>
                </div>
                <div class="detail-box">
                    <strong>🎓 Degree</strong>
                    <span>${rec.career_path?.recommended_degree || "Degree"}</span>
                </div>
            </div>

            <div class="accordion">
                <button class="accordion-btn">Why Recommended? ▼</button>
                <div class="panel">
                    ${explanationHTML}
                </div>

                <button class="accordion-btn">Education Path ▼</button>
                <div class="panel">
                    <p><strong>After 10th:</strong> ${rec.career_path?.after_10th_path || "N/A"}</p>
                    <p><strong>Entrance Exams:</strong> ${rec.entrance_exams ? rec.entrance_exams.join(", ") : "N/A"}</p>
                    <p><strong>Top Colleges:</strong> ${rec.top_colleges ? rec.top_colleges.join(", ") : "N/A"}</p>
                </div>
            </div>
        `;

        // Add accordion functionality
        card.querySelectorAll('.accordion-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                this.classList.toggle("active");
                var panel = this.nextElementSibling;
                if (panel.style.maxHeight) {
                    panel.style.maxHeight = null;
                } else {
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
            });
        });

        resultsDiv.appendChild(card);
    });

    // Trigger animations
    setTimeout(() => {
        const bars = document.querySelectorAll('.bar-fill');
        bars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 300);

    showNotification(`Found ${data.recommendations.length} career recommendations for you!`, "success");
}


/* ===============================
  Eligible Colleges Fetch (CET & NEET)
  =============================== */
async function checkColleges() {
    const examType = document.getElementById("exam").value;
    const percentile = document.getElementById("exam-percentile").value;
    const category = document.getElementById("category").value;
    const universityValue = document.getElementById("university")?.value;
    const cityValue = document.getElementById("city")?.value;
    const branchValue = document.getElementById("branch")?.value;

    // Convert empty strings to null for proper filtering
    const university = universityValue && universityValue.trim() !== "" ? universityValue : null;
    const city = cityValue && cityValue.trim() !== "" ? cityValue : null;
    const selectedBranch = branchValue && branchValue !== "AUTO" ? branchValue : null;

    // Validate inputs
    if (!percentile) {
        let examName = "CET";
        if (examType === "NEET") examName = "NEET";
        if (examType === "JEE") examName = "JEE";

        showNotification(
            `Please enter your ${examName} percentile to check eligible colleges.`,
            "warning"
        );
        return;
    }

    // Get career from AI card
    const careerElement = document.querySelector(".career-card h3");
    let career = selectedBranch ? selectedBranch :
        (examType === "NEET" ? "MBBS" : "Computer Engineering");

    if (careerElement) {
        // Remove emojis / symbols safely
        career = careerElement.innerText
            .replace(/[^\w\s]/gi, '')
            .trim();
    }

    // Show loading state
    const div = document.getElementById("collegeResults");
    let examName = "CET";
    if (examType === "NEET") examName = "NEET";
    if (examType === "JEE") examName = "JEE";

    div.innerHTML = `
        <div class="placeholder-message">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Searching eligible colleges based on ${examName}, category, and location...</p>
        </div>
    `;

    try {
        // Build request body with only non-null filter values
        const requestBody = {
            exam_type: examType,
            career: career,
            category_code: category
        };

        // Add User ID if logged in (for History)
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            requestBody.user_id = user.user_id;
        }

        // Add appropriate percentile field based on exam type
        if (examType === "NEET") {
            requestBody.neet_percentile = parseFloat(percentile);
        } else if (examType === "JEE") {
            requestBody.jee_percentile = parseFloat(percentile);
        } else {
            requestBody.cet_percentile = parseFloat(percentile);
        }

        // Only add filters if they have actual values
        if (university !== null) {
            requestBody.university_id = university;
        }
        if (city !== null) {
            requestBody.city = city;
        }
        // Add selected branch if user chose a specific one
        if (selectedBranch !== null) {
            requestBody.preferred_branch = selectedBranch;
        }

        const response = await fetch("http://127.0.0.1:5000/eligible-colleges", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();

        // Render results
        displayCollegeResults(data, percentile);

    } catch (error) {
        console.error("Error fetching college data:", error);

        showNotification(
            "Unable to connect to the server. Showing demo data instead.",
            "warning"
        );

        // Fallback demo data (UI demo-safe)
        showDemoCollegeData(percentile, category, career);
    }
}


/* ===============================
   Display College Results
   =============================== */
function displayCollegeResults(data, cet) {
    const div = document.getElementById("collegeResults");

    if (!data.eligible_colleges || data.eligible_colleges.length === 0) {
        div.innerHTML = `
            <h3>Eligible Colleges for ${data.career || "Your Career"} (${data.category || "Your Category"})</h3>
            <div class="placeholder-message">
                <i class="fas fa-university"></i>
                <p>No eligible colleges found for your percentile. Try a different percentile or category.</p>
            </div>
        `;
        return;
    }

    div.innerHTML = `<h3>Eligible Colleges for ${data.career} (${data.category})</h3>`;

    data.eligible_colleges.forEach((college, index) => {
        const card = document.createElement("div");
        card.className = "career-card";
        card.style.animationDelay = `${index * 0.1}s`;

        // Determine college tier by cutoff
        let tier = "Tier 2";
        let tierColor = "#3498db";
        if (college.cutoff_percentile > 95) {
            tier = "Tier 1";
            tierColor = "#2ecc71";
        } else if (college.cutoff_percentile < 75) {
            tier = "Tier 3";
            tierColor = "#e74c3c";
        }

        const isEligible = parseFloat(cet) >= parseFloat(college.cutoff_percentile);

        card.innerHTML = `
            <div class="college-header">
                <strong>${college.college_name}</strong>
                <span class="college-tier" style="background: ${tierColor}">${tier}</span>
            </div>
            <div class="college-details">
                <div class="detail-item">
                    <i class="fas fa-code-branch"></i>
                    <span>Branch: ${college.branch_name}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-chart-line"></i>
                    <span>Cutoff Percentile: <strong>${college.cutoff_percentile}</strong></span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-chair"></i>
                    <span>Available Seats: ${college.available_seats}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>Location: ${college.city || college.state || "Maharashtra"}</span>
                </div>
            </div>
            <div class="college-status">
                ${isEligible
                ? '<span class="status-eligible"><i class="fas fa-check-circle"></i> You are eligible</span>'
                : '<span class="status-ineligible"><i class="fas fa-times-circle"></i> You are not eligible</span>'}
            </div>
        `;

        div.appendChild(card);
    });

    showNotification(`Found ${data.eligible_colleges.length} colleges matching your criteria!`, "success");
}

/* ===============================
   Demo Data Functions
   =============================== */
function showDemoCareerData() {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    const demoData = {
        recommendations: [
            {
                career: "Software Engineer",
                description: "Design, develop, and maintain software systems and applications. Work with programming languages, frameworks, and development tools to create solutions for various industries.",
                suitability_score: 92,
                explanation: [
                    "Your interest in technology aligns perfectly with software development",
                    "Programming skills are highly valuable in this field",
                    "Strong mathematics background supports logical thinking required for software development",
                    "Problem-solving abilities match the daily challenges of software engineering"
                ]
            },
            {
                career: "Data Scientist",
                description: "Extract insights from complex data using statistical and machine learning techniques. Work with large datasets to solve business problems and drive decision-making.",
                suitability_score: 85,
                explanation: [
                    "Your analytical skills are ideal for data science roles",
                    "Interest in problem-solving matches data science challenges",
                    "Mathematics background provides strong foundation for statistical analysis",
                    "Technology interest aligns with data science tools and platforms"
                ]
            },
            {
                career: "AI/ML Engineer",
                description: "Build and deploy artificial intelligence and machine learning models. Specialize in developing algorithms that enable machines to learn and make intelligent decisions.",
                suitability_score: 78,
                explanation: [
                    "Technology interest aligns with cutting-edge AI field",
                    "Problem-solving skills essential for AI development challenges",
                    "Physics and mathematics background supports algorithm development",
                    "Programming skills provide foundation for implementing ML models"
                ]
            },
            {
                career: "Cybersecurity Analyst",
                description: "Protect computer systems and networks from cyber threats. Monitor security systems, investigate incidents, and implement security measures.",
                suitability_score: 65,
                explanation: [
                    "Problem-solving skills are crucial for identifying security vulnerabilities",
                    "Technology interest aligns with cybersecurity tools and techniques",
                    "Analytical thinking helps in threat detection and analysis"
                ]
            },
            {
                career: "Product Manager",
                description: "Lead product development from conception to launch, working with engineering, design, and marketing teams to deliver successful products.",
                suitability_score: 70,
                explanation: [
                    "Your problem-solving skills help in prioritizing features and roadmaps",
                    "Interest in technology aligns with product management in tech companies",
                    "Communication skills are essential for coordinating across teams"
                ]
            },
            {
                career: "Digital Marketing Specialist",
                description: "Plan and execute online marketing campaigns using SEO, social media, email, and content marketing to drive brand awareness and sales.",
                suitability_score: 60,
                explanation: [
                    "Creative thinking matches content creation and campaign design",
                    "Analytical skills help in measuring campaign performance",
                    "Interest in technology aligns with digital tools and platforms"
                ]
            }
        ]
    };

    displayCareerResults(demoData);
}

function showDemoCollegeData(cet, category, career) {
    const div = document.getElementById("collegeResults");
    div.innerHTML = `<h3>Eligible Colleges for ${career} (${category})</h3>`;

    const demoColleges = [
        {
            college_name: "College of Engineering, Pune",
            branch_name: career.includes("Computer") ? "Computer Engineering" : "Information Technology",
            cutoff_percentile: 95.5,
            available_seats: 120,
            location: "Pune"
        },
        {
            college_name: "VJTI Mumbai",
            branch_name: "Information Technology",
            cutoff_percentile: 96.2,
            available_seats: 80,
            location: "Mumbai"
        },
        {
            college_name: "SPIT Mumbai",
            branch_name: "Computer Engineering",
            cutoff_percentile: 97.1,
            available_seats: 60,
            location: "Mumbai"
        },
        {
            college_name: "KJ Somaiya College of Engineering",
            branch_name: "Artificial Intelligence & Data Science",
            cutoff_percentile: 92.3,
            available_seats: 90,
            location: "Mumbai"
        },
        {
            college_name: "MIT World Peace University",
            branch_name: "Computer Engineering",
            cutoff_percentile: 88.7,
            available_seats: 150,
            location: "Pune"
        },
        {
            college_name: "Sinhgad College of Engineering",
            branch_name: "Information Technology",
            cutoff_percentile: 85.4,
            available_seats: 180,
            location: "Pune"
        }
    ];

    // Filter colleges based on CET percentile (demo logic)
    const filteredColleges = demoColleges.filter(college =>
        parseFloat(cet) >= college.cutoff_percentile - 5
    );

    if (filteredColleges.length === 0) {
        div.innerHTML += `
            <div class="placeholder-message">
                <i class="fas fa-university"></i>
                <p>No eligible colleges found for your percentile (${cet}). Try a different percentile or category.</p>
            </div>
        `;
        return;
    }

    filteredColleges.forEach((college, index) => {
        const card = document.createElement("div");
        card.className = "career-card";
        card.style.animationDelay = `${index * 0.1}s`;

        // Determine college tier by cutoff
        let tier = "Tier 2";
        let tierColor = "#3498db";
        if (college.cutoff_percentile > 95) {
            tier = "Tier 1";
            tierColor = "#2ecc71";
        } else if (college.cutoff_percentile < 75) {
            tier = "Tier 3";
            tierColor = "#e74c3c";
        }

        const isEligible = parseFloat(cet) >= parseFloat(college.cutoff_percentile);

        card.innerHTML = `
            <div class="college-header">
                <strong>${college.college_name}</strong>
                <span class="college-tier" style="background: ${tierColor}">${tier}</span>
            </div>
            <div class="college-details">
                <div class="detail-item">
                    <i class="fas fa-code-branch"></i>
                    <span>Branch: ${college.branch_name}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-chart-line"></i>
                    <span>Cutoff Percentile: <strong>${college.cutoff_percentile}</strong></span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-chair"></i>
                    <span>Available Seats: ${college.available_seats}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>Location: ${college.location}</span>
                </div>
            </div>
            <div class="college-status">
                ${isEligible
                ? '<span class="status-eligible"><i class="fas fa-check-circle"></i> You are eligible</span>'
                : '<span class="status-ineligible"><i class="fas fa-times-circle"></i> You are not eligible</span>'}
            </div>
        `;

        div.appendChild(card);
    });
}

/* ===============================
   Notification System
   =============================== */
function showNotification(message, type = "info") {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;

    // Set icon based on type
    let icon = "ℹ️";
    if (type === "warning") icon = "⚠️";
    if (type === "success") icon = "✅";

    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span class="notification-text">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}