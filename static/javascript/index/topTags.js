$(document).ready(function () {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    let search_str = search_params.toString();

    let path = window.location.pathname;

    let topTagsURL = '/tags/top';
    // if (window.location.pathname !== '/') {
    //     topTagsURL += path;
    // } else
    if (search_str.length !== 0) {
        topTagsURL += "?" + search_str;
    }

    $.ajax({
        url: topTagsURL,
        type: 'GET',
        dataType: "json",
        success: function (data) {
            let topTags = data["tags"];
            $(topTags).each(function () {
                let topTag = this.name;
                let tagsBox = $(document.getElementById("tags__top__box"));
                tagsBox.append(`<li class="tags__top__box-decor" onclick='pickDisplay("tag","${topTag}")'>${topTag}</li>`);
            })
        },
        error: function () {
            alert('ERROR');
        }
    });
});
