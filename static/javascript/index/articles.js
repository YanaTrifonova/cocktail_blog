$(document).ready(function () {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    let search_str = search_params.toString();

    let path = window.location.pathname;

    let ajaxURL = '/articles';
    if (path.indexOf("/posts") !== -1) {
        let splitted = path.split("/");
        ajaxURL += "/" + splitted[splitted.length - 1];
    } else if (search_str.length !== 0) {
        ajaxURL += "?" + search_str;
    }

    $.ajax({
        url: ajaxURL,
        type: 'GET',
        dataType: "json",
        success: function (data) {
            let articles = data["articles"];

            $(articles).each(function () {
                let id = this.id;
                let title = this.title;
                let creationTime = this.creation_time;
                let body = this.body;
                let ingredients = this.ingredients;
                let tags = this.tags;

                $(".article").append(`<div id=${id} class='article__container'></div>`);

                let idSelector = $('#' + id);
                idSelector.append(`<h2 class='article__container__header' 
                                       onclick="articleDisplay('${id}')">${title}</h2>`);
                idSelector.append(`<p class='article__container__creationTime'>${creationTime}</p>`);
                idSelector.append(`<div class='article__container__body'>${body}</div>`);
                idSelector.append(`<ul class='article__container__tags'>Tags:</ul>`);

                let tagsSelector = $('#' + id + `>.article__container__tags`);
                ingredients.forEach(function (ingredient) {
                    tagsSelector.append(`<li class='article__container__tags__elem' 
                                             onclick='pickDisplay("tag","${ingredient}")'>${ingredient}</li>`);
                });
                tags.forEach(function (tag) {
                    tagsSelector.append(`<li class='article__container__tags__elem' 
                                             onclick='pickDisplay("tag","${tag}")'>${tag}</li>`);
                });

            });
            PaginationLoader();

            let prev = data["has_previous"];
            let next = data["has_next"];
            if (!prev) {
                $('#prev').addClass(" paginations__hidden");
            }
            if (!next) {
                $('#next').addClass(" paginations__hidden");
            }

            FooterLoader();
        },
        statusCode: {
            500: function () {
                alert('ERROR'); // build new
            },

            404: function () {
                alert('return 404'); // build new
            }
        },
        error: function () {
            alert('ERROR');
        },
    });


});