/*Function that display articles with chosen tag or with value that get from search*/

function pickDisplay(p, value) {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    search_params.set(p, value);
    if (search_params.has("offset")) {
        search_params.set("offset", '0');
    }
    window.location.href = '?' + search_params.toString();
}