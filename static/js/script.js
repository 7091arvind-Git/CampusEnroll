/**
 * CampusEnroll - Student Course Registration System
 * Vanilla JavaScript Helpers
 * 
 * Features:
 * - Theme Switcher (Light / Dark / System Default)
 * - Auto-dismiss Flash Alerts
 * - Real-time client-side search
 * - Modal & Confirmation dialogs
 */

// ==============================================================================
// THEME SWITCHER LOGIC (Light / Dark / System Mode)
// ==============================================================================
function getPreferredTheme() {
    return localStorage.getItem('theme') || 'system';
}

function setTheme(theme) {
    localStorage.setItem('theme', theme);
    applyTheme(theme);
}

function applyTheme(theme) {
    let resolvedTheme = theme;
    if (theme === 'system') {
        resolvedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-bs-theme', resolvedTheme);
    document.documentElement.setAttribute('data-theme-setting', theme);
    updateThemeUI(theme, resolvedTheme);
}

function updateThemeUI(themeSetting, resolvedTheme) {
    const icon = document.getElementById('themeActiveIcon');
    const text = document.getElementById('themeActiveText');
    if (!icon) return;

    if (themeSetting === 'light') {
        icon.className = 'bi bi-sun-fill text-warning';
        if (text) text.textContent = 'Light';
    } else if (themeSetting === 'dark') {
        icon.className = 'bi bi-moon-stars-fill text-primary';
        if (text) text.textContent = 'Dark';
    } else {
        icon.className = 'bi bi-circle-half text-secondary';
        if (text) text.textContent = 'System';
    }
}

// Listen for OS system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (getPreferredTheme() === 'system') {
        applyTheme('system');
    }
});

// ==============================================================================
// DOM READY INITIALIZATIONS
// ==============================================================================
document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Theme UI
    const currentTheme = getPreferredTheme();
    applyTheme(currentTheme);

    // 2. Auto-dismiss Bootstrap flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (alert && alert.classList.contains('show')) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // 3. Client-side Real-time Search for Course Cards on courses.html
    const courseSearchInput = document.getElementById('clientCourseSearch');
    if (courseSearchInput) {
        courseSearchInput.addEventListener('input', function (e) {
            const query = e.target.value.toLowerCase().trim();
            const courseCards = document.querySelectorAll('.course-item');

            let visibleCount = 0;
            courseCards.forEach(function (card) {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = '';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            const noResultsMsg = document.getElementById('noResultsMessage');
            if (noResultsMsg) {
                noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
            }
        });
    }

    // 4. Client-side Table Search for Admin Tables (Students, Courses, Registrations)
    const tableSearchInput = document.getElementById('clientTableSearch');
    if (tableSearchInput) {
        tableSearchInput.addEventListener('input', function (e) {
            const query = e.target.value.toLowerCase().trim();
            const tableRows = document.querySelectorAll('.searchable-table tbody tr');

            tableRows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // 5. Initialize LocalStorage Course Bookmarks
    initBookmarks();
});

// ==============================================================================
// LOCAL STORAGE PERSISTENCE: COURSE WISHLIST & BOOKMARKING
// ==============================================================================
function getSavedCourses() {
    try {
        return JSON.parse(localStorage.getItem('campusenroll_saved_courses') || '[]');
    } catch (e) {
        return [];
    }
}

function updateBookmarkCounts() {
    const saved = getSavedCourses();
    const countEl = document.getElementById('savedCount');
    if (countEl) {
        countEl.textContent = saved.length;
    }
}

function toggleBookmark(courseId, btn) {
    let saved = getSavedCourses();
    const numId = parseInt(courseId, 10);
    const index = saved.indexOf(numId);
    
    if (index === -1) {
        saved.push(numId);
        btn.innerHTML = '<i class="bi bi-star-fill text-warning"></i>';
        btn.setAttribute('title', 'Remove from Saved Courses (Local Storage)');
    } else {
        saved.splice(index, 1);
        btn.innerHTML = '<i class="bi bi-star"></i>';
        btn.setAttribute('title', 'Save to Wishlist (Local Storage)');
    }
    
    localStorage.setItem('campusenroll_saved_courses', JSON.stringify(saved));
    updateBookmarkCounts();
}

function initBookmarks() {
    const saved = getSavedCourses();
    document.querySelectorAll('.bookmark-btn').forEach(btn => {
        const id = parseInt(btn.getAttribute('data-course-id'), 10);
        if (saved.includes(id)) {
            btn.innerHTML = '<i class="bi bi-star-fill text-warning"></i>';
            btn.setAttribute('title', 'Remove from Saved Courses (Local Storage)');
        }
    });
    updateBookmarkCounts();
}

function filterWishlist(showOnlyWishlist) {
    const saved = getSavedCourses();
    const allBtn = document.getElementById('filterAllBtn');
    const wishBtn = document.getElementById('filterWishlistBtn');
    
    if (allBtn && wishBtn) {
        if (showOnlyWishlist) {
            allBtn.classList.remove('active');
            wishBtn.classList.add('active');
        } else {
            allBtn.classList.add('active');
            wishBtn.classList.remove('active');
        }
    }
    
    document.querySelectorAll('.course-item').forEach(card => {
        const id = parseInt(card.getAttribute('data-course-id'), 10);
        if (showOnlyWishlist) {
            card.style.display = saved.includes(id) ? '' : 'none';
        } else {
            card.style.display = '';
        }
    });
}

// ==============================================================================
// CONFIRMATION DIALOGS
// ==============================================================================
/**
 * Confirmation dialog before dropping a course.
 */
function confirmDropCourse(courseCode) {
    return confirm("Are you sure you want to drop course " + courseCode + "?\nThis will free up your seat and credit allocation.");
}

/**
 * Confirmation dialog before deleting a course (Admin).
 */
function confirmDeleteCourse(courseCode) {
    return confirm("WARNING: Are you sure you want to delete course " + courseCode + "?\nThis will also remove all student registrations for this course!");
}
