$(document).ready(function(){

$("#add").click(function(e){
    event.preventDefault();
    $("#items").append('<div class="wrap-input100 validate-input m-b-23" data-validate = "input is reauired">\
    <input class="label-input100" type="text" name="node_val" placeholder="Enter new node value">\
    <input class="input100" type="text" name="node_type" placeholder="Enter modified node type">\
    <input class="input100" type="text" name="node_sql" placeholder="Enter modified word in SQL">\
    <input type="button" value="delete" id="delete"></div>');
});

$("body").on("click", "#delete", function(e) {
    $(this).parent('div').remove()
})

});