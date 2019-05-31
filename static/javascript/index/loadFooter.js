function FooterLoader() {
    let body = $('body');
    body.append(`<footer class="footer"></footer>`);
    $('.footer').append(`<div class="footer__btn"></div>`);
    let foot = $('.footer__btn');
    foot.append(`<span class="footer__btn-decor"><a class="footer__btn-text" href="ingredients">Ingredients</a></span>`);
    foot.append(`<span class="footer__btn-decor"><a class="footer__btn-text" href="list">List</a></span>`);
    foot.append(`<span class="footer__btn-decor"><a class="footer__btn-text" href="about">About</a></span>`);
    foot.append(`<span class="footer__btn-decor"><a class="footer__btn-text" href="contactUs">Contact Us</a></span>`);
}