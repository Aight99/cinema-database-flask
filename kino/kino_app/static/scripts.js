const navbar = document.getElementById("navbar");
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