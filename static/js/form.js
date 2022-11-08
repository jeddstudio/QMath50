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
            // pasuse the stopwatch
            clearInterval(Interval);
        }        
        else {
            // If the answer is wrong, Clear the input field, lets user keep trying
            $("#setForm")[0].reset();
        }
});
    e.preventDefault();
});


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
            }
        })
    })
})

