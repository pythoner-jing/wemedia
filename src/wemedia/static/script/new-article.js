$(document).ready(function(){
    var editor = UM.getEditor("editor");
    var $plain_text = $("#plain_text");

    function _add_plain_text(){
        $plain_text.val(editor.getPlainTxt());
        alert($plain_text.val());
    }

    add_plain_text = _add_plain_text;
});