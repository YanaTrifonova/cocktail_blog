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
                    $("#Other").append(`<li class='alphabet__character__tag'>${chr}</li>`);
                } else {
                    $("#"+res).append(`<li class='alphabet__character__tag'>${chr}</li>`);
                }
            }
        }
    })
})