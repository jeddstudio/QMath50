$('#setForm').submit(function(e) {

    $.ajax({
        data : {
            guess : $('#guess').val()
        },
        type : 'POST',
        url : '/game'
//        document.getElementByName("#guess").reset();
    })
    .done(function(data) {

    if (data.display_number) {
//        $('#display_num_L').text(data.display_number).show();
        $('#display_num_R').text(data.display_number).show();
//        $('#successAlert').hide();
        $("#setForm")[0].reset();
    }
    else {
        $("#setForm")[0].reset();
//        $('#GuessAlert').text(data.set).show();
//        $('#lowAlert').text(data.lowest).show();
//        $('#highAlert').text(data.highest).show();
//        $('#guessNumber').text(data.guesses).show();
//
//        $('#lowInput, #highInput').attr('readOnly','true');
//        $('#guesInput').prop('readOnly','');
//
//
//        $("#setButton").attr("disabled", 'true');
//        $('#GuessButton').prop('disabled','');
//
//        $('#guessBox').css('display', '');
//        $('#toLowInput').hide();
//        $('#errorAlert').hide();
    }
});
//    $.ajax({
//    .clear(function(e) {
//        document.getElementByName("#guess").reset();
//        });
//    })
    e.preventDefault();
});


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
                $('#display_num_L').text(response.js_number_L)
                // let the user input in input field
                $("#guess").attr("disabled",false); 
                $(".page-link").attr("disabled",true).css("pointer-events","none");
            }
        })
    })
})

