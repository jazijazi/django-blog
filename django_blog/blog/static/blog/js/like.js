$(document).ready(function () {
    ////////////////////////////* becuse CSRF get error on ajax post  *//////////////////////////////////
    // This will allow to get csrf token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // This will send csrf token on every ajax request
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    ////////////////////////////* becuse CSRF get error on ajax post  *//////////////////////////////////
    
    $(".likebtn").click(function () {
        var pk = $(this).attr("pk") ;
        $.post("/like_post/", { pk: pk }, function (data) {
            if(data.liked == "True"){
                console.log("like successful");
                $("a[pk=" + pk + "]").children().css("color","red");                
            }
            else if (data.disliked == "True") {
                console.log("dislike successful");
                $("a[pk=" + pk + "]").children().css("color", "#cebdbd");                

            }
            else{
                alert("Error in like or dislike this post");  
            }
        }).done(function () {
            console.log("like or dislike request done");
        }).fail(function () {
            alert("Fail for requset like or dislike this post");
        });
    });
});