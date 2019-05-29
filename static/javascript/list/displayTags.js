$(document).ready(function () {
    $.ajax({
        url: '/tags',
        type: 'GET',
        dataType: "json",
        success: function (data) {
            let tags = data['tags'];
            for (let x in tags) {
                let chr = tags[x].name;
                let chrUpperCase = chr.toUpperCase();
                let res = chrUpperCase.charAt(0);
                if(res.toUpperCase() === res.toLowerCase()) {
                    let other = $("#Other");
                    other.append(`<li class='alphabet__container__tag' onclick='pickDisplay("tag","${chr}")'>${chr}</li>`);
                    other.parent().addClass("alphabet__container-display");
                } else {
                    let char = $("#"+res);
                    char.parent().addClass("alphabet__container-display");
                    char.append(`<li class='alphabet__container__tag' onclick='pickDisplay("tag","${chr}")'>${chr}</li>`);
                }
            }
            FooterLoader();
        }
    });
});