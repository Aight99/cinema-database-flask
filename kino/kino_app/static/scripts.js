const navbar = document.getElementById("navbar");
const loginButton = document.getElementById("login");
const loginPopup = document.getElementById("login-popup")
loginPopup.addEventListener('click', () => loginPopup.close());
const popupBody = document.getElementById('popup-body');
popupBody.addEventListener('click', (event) => event.stopPropagation());
// const navbar = document.getElementById("navbar");

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

loginButton.addEventListener("click", () => {
  loginPopup.showModal();
});

// loginPopup.addEventListener('click', (event) => {
//     if (event.target.id !== 'popup-body') {
//         loginPopup.close();
//     }
// });