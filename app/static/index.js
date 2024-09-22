//Navbar Toggler Icon Switch JS 
const navbarToggler = document.getElementById('navbar-toggler');
const navbarIcon = document.getElementById('navbar-icon');

navbarToggler.addEventListener('click', function() {
    // Toggle between fa-bars (hamburger) and fa-times (X)
    if (navbarIcon.classList.contains('fa-bars')) {
        navbarIcon.classList.remove('fa-bars');
        navbarIcon.classList.add('fa-times');
    } else {
        navbarIcon.classList.remove('fa-times');
        navbarIcon.classList.add('fa-bars');
    }
});