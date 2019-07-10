function menu() {
    let m = document.querySelector("#menuBtn");
    let h = document.querySelector("#header");
    let b = document.querySelector("menuBar");

    let burger = document.querySelector("#burger");
    let crossMenu = document.querySelector("#crossMenu");

    if (!(m.classList.contains("nav__details__btn-menu"))) {
        m.classList.add("nav__details__btn-menu");
        m.classList.remove("nav__details__btn-hidden");
        h.classList.add("nav__details__header-mobile");
        burger.classList.remove("fas", "fa-bars", "nav__details__btn-mobile-pic");
        crossMenu.classList.add("fas", "fa-times", "nav__details__btn-mobile-pic");

    } else {
        m.classList.remove("nav__details__btn-menu");
        m.classList.add("nav__details__btn-hidden");
        h.classList.remove("nav__details__header-mobile");
        burger.classList.add("fas", "fa-bars", "nav__details__btn-mobile-pic");
        crossMenu.classList.remove("fas", "fa-times", "nav__details__btn-mobile-pic");
    }
}