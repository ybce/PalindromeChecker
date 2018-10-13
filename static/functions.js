


function checkPalindrome(message_id){
    $.ajax({
    type: "POST",
    url: "http://localhost:5000/check/",
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

function deleteMessage(message_id){
    $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/delete/",
    // The key needs to match your method's input parameter (case-sensitive).
    data: JSON.stringify({ "message_id": message_id }),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){
        id = '#'+message_id;
        $(id).remove();
        },
    failure: function(errMsg) {
        console.log("Error");
        console.log(errMsg);
    }
});
}

$( "#add-message" ).submit(function( event ) {
  var data = $('#add-message').serializeArray()[0];
  $.ajax({
    type: "POST",
    url: "http://localhost:5000/add/",
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
            "<td id="+boolid+"><button onclick='checkPalindrome("+id+")'>Check if Palindrome</button></td>" +
            "<td><button onclick=deleteMessage("+id+")>Delete this message</button></td>" +
            "</tr>";
        $('#message-table').append(markup);
        //document.getElementById("message-table").insertRow(-1).innerHTML = markup;

    },
    failure: function(errMsg) {
        console.log("Error");
        console.log(errMsg);
    }});
  $('#message-input').trigger(':reset');
  event.preventDefault();
});