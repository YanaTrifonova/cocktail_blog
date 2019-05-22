function saveForm() {
    var dataOut =
        {
            title: $('#header').val(),
            body: $("#note").summernote('code'),
            is_cocktail: $('#isCocktail').is(":checked"),
            user_id: 1,
            tags: $('#tags').val().split(", "),
            ingredients: $('#ingr').val().split(", "),
            cocktail_name: $('#cocktailName').val(),
        };
    dataOut.tags.forEach(function (tag, ind, arr) {
        arr[ind] = tag.trim();
    });
    dataOut.ingredients.forEach(function (ingredient, ind, arr) {
        arr[ind] = ingredient.trim();
    });
    $.ajax({
        url: '/articles',
        type: 'PUT',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(dataOut),
        success: function () {
            alert('Load was performed.');
        },
        error: function () {
            alert('ERROR');
        }
    });
}
