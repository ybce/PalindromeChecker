
$(document).ready(function () {



function checkPalindrome (message_id) {
    $.ajax({
    type: "POST",
    url: "/check/",
    // The key needs to match your method's input parameter (case-sensitive).
    data: JSON.stringify({ "message_id": message_id }),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
        id = '#bool'+data.message_id;
        console.log(data.palindrome);
        if(data.palindrome == "1"){
         $(id).text("Yes");
        }
        else if(data.palindrome == "0"){
            $(id).text("No");
        }
        },
    failure: function(errMsg) {
        console.log("Error");
        console.log(errMsg);
    }
});
}



function deleteRow(message_id){

    $.ajax({
        type: "DELETE",
        url: "/delete/",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify({"message_id": message_id}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            id = '#' + message_id;
            $(id).remove();
        },
        failure: function (errMsg) {
            console.log("Error");
            console.log(errMsg);
        }
    });
}

$(document).on("click", "button",function (event) {
    var b_id = this.id;

    var action = b_id.split('-')[0];

    var message_id = b_id.split('-')[1];

    if (action === 'delete') {
        deleteRow(message_id);
    }
    else if(action === 'check'){
        checkPalindrome(message_id)
    }
    event.preventDefault();
});

$( "#add-message" ).submit(function( event ) {
  var data = $('#add-message').serializeArray()[0];
  $("#message-input").val("");
  $.ajax({
    type: "POST",
    url: "/add/",
    // The key needs to match your method's input parameter (case-sensitive).
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
        var id = data.message_id;
        var boolid = "bool"+data.message_id;
        var message = data.message;
        var markup = "<tr id="+id+">" +
            "<td>"+message+"</td>" +
            "<td id="+boolid+"><button id='check-"+id+"'>Check if Palindrome</button></td>" +
            "<td><button id='delete-"+id+"'>Delete this message</button></td>" +
            "</tr>";
        $('#message-table').append(markup);
        //document.getElementById("message-table").insertRow(-1).innerHTML = markup;

    },
    failure: function(errMsg) {
        console.log("Error");
        console.log(errMsg);
    }});
  event.preventDefault();
});

});