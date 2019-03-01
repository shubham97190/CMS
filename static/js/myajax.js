function myfunc(){
        $.ajax({
            url:'/get_state',
            data:$('#country'),
            type:'GET',
            dataType:'json',
            success:function(response){
                if(response.type == 'get_state'){
                    console.log(response.result);
                    $("#state").html('');
                    $("#state").append('<option value="0">(please select a State)</option>');
                    $.each(response.result, function(key, val) {

                        $("#state").append("<option value="+val['id']+">"+val['name']+"</option>");
                    });
                }
            },
            error:function(error){
                console.log(error);
            }
        });
   }

function getCity(){
    $.ajax({
        url:'/get_city',
        data:$('#state'),
        type:'GET',
        dataType:'json',
        success:function(response){
            if(response.type == 'get_city'){
                $("#city ").html('');
                $("#city").append('<option value="0">(please select a City)</option>');
                $.each(response.result, function(key, val) {
                    $("#city ").append("<option value="+val['id']+">"+val['name']+"</option>");
                });
            }
        },
        error:function(error){
            console.log(error);
        }
    });
}

function check_user(){
    $.ajax({
        url:'/check_user',
        data:$('#uname'),
        type:'GET',
        dataType:'json',
        success:function(response){
            if(response.type == 'check_user'){
                $(".u_error").html('');
                if(response.result != null){
                $('#uname').after('<span class="u_error" style="color:red;">That username is Taken . Try another</span>');
                }
            }
        },
        error:function(error){
            console.log(error);
        }
    });
}

function check_email(){
    $.ajax({
        url:'/check_email',
        data:$('#email'),
        type:'GET',
        dataType:'json',
        success:function(response){
            if(response.type == 'check_email'){
                $(".e_error").html('');
                if(response.result != null){
                $('#email').after('<span class="e_error" style="color:red;">That Email is Taken . Try another</span>');
                }
            }
        },
        error:function(error){
            console.log(error);
        }
    });
}
