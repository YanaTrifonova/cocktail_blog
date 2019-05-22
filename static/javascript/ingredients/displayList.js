$(document).ready(function () {
    $.ajax({
        url: '/cocktails',
        type: 'GET',
        dataType: "json",
        success: function (data) {
            let cocktails = data['cocktails'];
            let ingredient = Object.keys(cocktails);
            for (var x in ingredient) {
                $("#list").append(`<div id=${ingredient[x]} class='cocktailList__container'></div>`);
                let containerSelector = $('#' + ingredient[x]);
                containerSelector.append(`<h2 class='cocktailList__container__header' onclick="pickDisplay('tag', '${ingredient[x]}')">${ingredient[x]}</h2>`);
                $(cocktails[ingredient[x]]).each(function () {
                    let id = this.id;
                    let cocktailName = this.name;
                    containerSelector.append(`<p class='cocktailList__container__name' 
                                                 onclick="articleDisplay('${id}')">${cocktailName}</p>`);
                })
            }
        },
    })
});