// Ajax function
$('#setForm').submit(function(e) {

    $.ajax({
        data : {
            js_guess : $('#guess').val(),
        },
        type : 'POST',
        url : '/game'
    })

    // When user input a num then press Enter
    .done(function(data) {
        if (data.js_display_number) {
            console.log("R_numb changing")
            // Hide the input prompt
            $('#inputPrompt').hide();
            // Right number change and clear the input field
            $('#display_num_R').text(data.js_display_number).show();
            // Clear the input field
            $("#setForm")[0].reset();
        }

        // When user finished 1-10, will pass a counter from Flask
        if (data.endGame) {
            console.log("Game end")
            
            // show a message
            $('#GuessAlert').text(data.endGame).show();
            $("#setForm")[0].reset();
            $("#guess").attr("disabled",true); 
            // Activate L number selector again
            $(".page-link").attr("disabled",false).css("pointer-events","auto");
            // Popup the "select a number again" prompt
            $('#playAgainPrompt').show();
            console.log("Game end code Done")

            // When the uesr click num_L button, hide the prompt and Alert
            $('.page-link').click(function(){
                // hide the result alert box
                $('#GuessAlert').text(data.endGame).hide();
                // hide the "select a number again" prompt
                $('#playAgainPrompt').hide();
            })
            // After that, it will go to "L number selector" function and keep programme running
        }        
        else {
            // If the answer is wrong, Clear the input field, lets user keep trying
            $("#setForm")[0].reset();
        }
});
    e.preventDefault();
});

//////////////////////////////
// Ajax function
$('#logForm').submit(function(e) {

    $.ajax({
        data : {
            username : $('#username').val(),
            password : $('#password').val()
        },
        type : 'POST',
        url : '/register'
    })

    // When user input a num then press Enter
    .check(function(data) {

        // When user finished 1-10, will pass a counter from Flask
        if (data.usernameprompt) {
            console.log("usernameprompt")
            
            // show a message
            $('#missUsernamePrompt').text(data.usernameprompt).show();
            $("#logForm")[0].reset();

            // $("#guess").attr("disabled",true); 
            // // Activate L number selector again
            // $(".page-link").attr("disabled",false).css("pointer-events","auto");
            // // Popup the "select a number again" prompt
            // $('#playAgainPrompt').show();
            // console.log("Game end code Done")

            // // When the uesr click num_L button, hide the prompt and Alert
            // $('.page-link').click(function(){
            //     // hide the result alert box
            //     $('#GuessAlert').text(data.endGame).hide();
            //     // hide the "select a number again" prompt
            //     $('#playAgainPrompt').hide();
            // })
            // After that, it will go to "L number selector" function and keep programme running
        }        
        else {
            // If the answer is wrong, Clear the input field, lets user keep trying
            $("#logForm")[0].reset();
        }
});
    e.preventDefault();
});





//////////////////////////////




// L number selector
$(document).click(function(){
    $('.page-link').click(function(){
        $.ajax({
            url:'',
            type:'get',
            contentType: 'application/json',
            data: {
                number_L: $(this).data('value')
            },
            success: function(response){
                $('.number_L').data('value')
                // Show num_L that the user choose on the webpage
                $('#display_num_L').text(response.js_number_L)
                // Enable and let the user input in input field
                $("#guess").attr("disabled",false); 
                // Disable the L number selector
                $(".page-link").attr("disabled",true).css("pointer-events","none");
                // hide the num_L prompt
                $('#numLPrompt').hide();
                // 
                $('#inputPrompt').show();
            }
        })
    })
})

