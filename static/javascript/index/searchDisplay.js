function searchBtnClicked() {
    let elem = document.querySelector("#mySearch");
    let s = document.querySelector("#search");
    let x = document.querySelector("#crossSearch");
    let menuB = document.querySelector("#menuBar");
    let b = document.querySelector("menuBar");

    if (!(elem.classList.contains("nav__details__search-mobile"))) {
        elem.classList.add("nav__details__search-mobile");
        elem.classList.remove("nav__details__search-box");
        s.classList.add("nav__details__search-pic-hidden");
        s.classList.remove("fa", "fa-search", "nav__details__search-pic");
        x.classList.remove("nav__details__search-pic-hidden");
        x.classList.add("fas", "fa-times", "nav__details__search-pic");
        menuB.classList.remove("nav__details__btn-mobile");
        menuB.classList.add("nav__details__btn-hidden");
        b.classList.remove("fas", "fa-bars", "nav__details__btn-mobile-pic");
    } else {
        elem.classList.remove("nav__details__search-mobile");
        elem.classList.add("nav__details__search-box");
        s.classList.remove("nav__details__search-pic-hidden");
        x.classList.add("nav__details__search-pic-hidden");
        x.classList.remove("fas", "fa-times", "nav__details__search-pic");
        s.classList.add("fa", "fa-search", "nav__details__search-pic");
        menuB.classList.add("nav__details__btn-mobile");
        menuB.classList.remove("nav__details__btn-hidden");
        b.classList.remove("fas", "fa-bars", "nav__details__btn-mobile-pic");
    }
}