$(document).ready(function () {
    if ((navigator.userAgent.toLowerCase().indexOf('firefox')) === -1) {
        $(".contactUs").addClass("contactUs-fix");
    } else {
        $(".contactUs").addClass("contactUs-fixFF")
    }
});