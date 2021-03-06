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
    dataOut.tags = dataOut.tags.filter(function (val, ind, arr) {
        return val !== ""

    });
    dataOut.ingredients.forEach(function (ingredient, ind, arr) {
        arr[ind] = ingredient.trim();
    });
    dataOut.ingredients = dataOut.ingredients.filter(function (val, ind, arr) {
        return val !== ""
        
    });
    $.ajax({
        url: '/articles',
        type: 'PUT',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(dataOut),
        success: function () {
            location.href = "/";
        },
        error: function () {
            alert('ERROR');
        }
    });
}
