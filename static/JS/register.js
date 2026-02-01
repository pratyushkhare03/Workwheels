const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

/* ---------- button clicks (keep animation) ---------- */
registerBtn.addEventListener('click', () => {
    container.classList.add('active');      // animation
    history.pushState({ form: 'register' }, '', '/register/');
});

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');   // animation
    history.pushState({ form: 'login' }, '', '/login/');
});

/* ---------- handle back / forward navigation ---------- */
window.addEventListener('popstate', () => {
    if (location.pathname.includes('register')) {
        container.classList.add('active');
    } else {
        container.classList.remove('active');
    }
});

/* ---------- fix initial load (page refresh / restore) ---------- */
document.addEventListener('DOMContentLoaded', () => {
    if (location.pathname.includes('register')) {
        container.classList.add('active');
    } else {
        container.classList.remove('active');
    }
});
