/*Display tags that has been chosen by user*/

function tagsDisplay(tagToDisplay) {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    search_params.set("tag", tagToDisplay);
    if (search_params.has("offset")) {
        search_params.set("offset", '0');
    }
    window.location.href = '?' + search_params.toString();
}

/*Display one particular article that has been chosen by user*/

function articleDisplay(idToDisplay) {
    window.location.href = '/' + idToDisplay;

    let hiddenPrev = document.getElementById("prev");
    hiddenPrev.className += " paginations__hidden";

    let hiddenNext = document.getElementById("next");
    hiddenNext.className += " paginations__hidden";
}

