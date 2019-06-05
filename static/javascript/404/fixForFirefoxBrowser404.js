$(document).ready(function () {
    if ((navigator.userAgent.toLowerCase().indexOf('firefox')) === -1) {
        $(".pageNotFound").addClass("pageNotFound-fix");
    } else {
        $(".pageNotFound").addClass("pageNotFound-fixFF")
    }
});