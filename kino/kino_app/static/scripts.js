const navbar = document.getElementById("navbar");

const loginButton = document.getElementById("login");
loginButton.addEventListener("click", () => loginPopup.showModal());
const loginPopup = document.getElementById("login-popup")
loginPopup.addEventListener('click', () => loginPopup.close());
const popupBody = document.getElementById('popup-body');
popupBody.addEventListener('click', (event) => event.stopPropagation());

const signupButton = document.getElementById("signup");
signupButton.addEventListener("click", () => signupPopup.showModal());
const signupPopup = document.getElementById("signup-popup")
signupPopup.addEventListener('click', () => signupPopup.close());
const signupPopupBody = document.getElementById('signup-popup-body');
signupPopupBody.addEventListener('click', (event) => event.stopPropagation());

let prevScrollPosition = window.scrollY;

window.onscroll = function () {
    let currentScrollPosition = window.scrollY;
    if (prevScrollPosition > currentScrollPosition) {
        navbar.style.top = "0";
    } else {
        navbar.style.top = "-80px";
    }
    prevScrollPosition = currentScrollPosition;
}

function goToMovie(movie_id) {
    location.href = "/movie/" + movie_id;
}