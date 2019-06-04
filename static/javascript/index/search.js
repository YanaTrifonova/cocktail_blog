function submit() {
    let searchInput = $('#mySearch').val();
    pickDisplay("search", searchInput);
}

function enterPressed(e) {
    if (e.which === 13) {
        submit();
    }
}