$(document).ready(function () {
    $('#note').summernote();
});
var edit = function () {
    $('.click2edit').summernote({focus: true});
};

var save = function () {
    var markup = $('.click2edit').summernote('code');
    $('.click2edit').summernote('destroy');
};