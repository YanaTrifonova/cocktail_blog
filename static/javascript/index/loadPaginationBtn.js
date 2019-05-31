function PaginationLoader() {
    let body = $('body');
    body.append(`<div class="paginations"></div>`);
    let pag = $('.paginations');
    pag.append(`<a class="paginations__btn" href="#" id="prev" onclick="previousPage()"><i class="fal fa-chevron-left paginations__btn-chevron paginations__btn-chevron-left"></i>previous</a>`);
    pag.append(`<a class="paginations__btn" href="#" id="next" onclick="nextPage()">next<i class="fal fa-chevron-right paginations__btn-chevron paginations__btn-chevron-right"></i></a>`);
}
