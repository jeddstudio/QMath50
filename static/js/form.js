// // Variable for Stopwatch function
// const appendMsSeconds = document.getElementById("ms_sec")
// const appendSeconds = document.getElementById("seconds")



// let seconds = 00; 
// let ms_seconds = 00; 
// let last_ms_seconds = document.getElementById("ms_sec").innerText;
// let Interval;

// // Get user input from HTML
// const guessInput = document.querySelector("#guess");


// Ajax function
$('#setForm').submit(function(e) {

    $.ajax({
        data : {
            js_guess : $('#guess').val(),
            // js_seconds : seconds,
            // js_ms_seconds : document.getElementById("ms_sec").innerText
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
            console.log("End Game")
            // show a message
            $('#GuessAlert').text(data.endGame).show();
            // pasuse the stopwatch
            clearInterval(Interval);
            // last_ms_seconds = document.getElementById("ms_sec").innerText;
            // console.log(last_ms_seconds);
        }        
        else {
            // If the answer is wrong, Clear the input field
            // lets user keep trying
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


// START the Stopwatch Function with input and press Enter
guessInput.addEventListener("keypress", function (e) {
    if (e.key === 'Enter') {
        clearInterval(Interval);
        Interval = setInterval(startTimer, 10);
        console.log("TIMER START")
    }
})

// Stopwatch Function
// Display and counting the stopwatch on the webpage
function startTimer () {
    ms_seconds++; 
    
    if(ms_seconds <= 9){
        appendMsSeconds.innerHTML = "0" + ms_seconds;
    }
    
    if (ms_seconds > 9){
        appendMsSeconds.innerHTML = ms_seconds;
    } 
    
    if (ms_seconds > 99) {
      console.log("seconds");
      seconds++;
      appendSeconds.innerHTML = "0" + seconds;
      ms_seconds = 0;
      appendMsSeconds.innerHTML = "0" + 0;
    }
    
    if (seconds > 9){
      appendSeconds.innerHTML = seconds;
    }
  }