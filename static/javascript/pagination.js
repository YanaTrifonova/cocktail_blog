function previousPage() {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    if (search_params.has("offset")) {
        search_params.set('offset', parseInt(search_params.get('offset')) - 5);
    }
    window.location.href = '?' + search_params.toString();
}

function nextPage() {
    let url = new URL(window.location);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    if (search_params.has("offset")) {
        search_params.set('offset', parseInt(search_params.get('offset')) + 5);
    } else {
        search_params.set("offset", '5');
    }
    window.location.href = '?' + search_params.toString();
}