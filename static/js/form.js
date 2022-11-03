
// Variable for Stopwatch function
const timeDisplay = document.querySelector("#timeDisplay");
// const startBtn = document.querySelector("#startBtn");
// const pauseBtn = document.querySelector("#pauseBtn");
// const resetBtn = document.querySelector("#resetBtn");


const guessInput = document.querySelector("#guess");

// const numBtnL = document.querySelector(".page-link")

let startTime = 0;
let elapsedTime = 0;
let currentTime = 0;
let paused = true;
let intervalId;
let hrs = 0;
let mins = 0;
let secs = 0;


// Ajax function
$('#setForm').submit(function(e) {

    $.ajax({
        data : {
            guess : $('#guess').val()
        },
        type : 'POST',
        url : '/game'

    })
    // When user input a num then press Enter
    // Right number change and clear the input field
    .done(function(data) {
        if (data.js_display_number) {
            $('#display_num_R').text(data.js_display_number).show();
            $("#setForm")[0].reset();
        }
        // When user finished 1-10, Flask will pass a counter
        // pause the stopwatch and show a message
        if (data.endGame) {
            console.log("End Game")
            // show a message
            $('#GuessAlert').text(data.endGame).show();
            // pasuse the stopwatch
            if(!paused){
                paused = true;
                elapsedTime = Date.now - startTime;
                clearInterval(intervalId);
            }
        }        
        else {
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
                $('#display_num_L').text(response.js_number_L)
                // let the user input in input field
                $("#guess").attr("disabled",false); 
                $(".page-link").attr("disabled",true).css("pointer-events","none");
            }
        })
    })
})

// Stopwatch Function with input and press Enter
guessInput.addEventListener("keydown", () => {
    if(paused){
        console.log("Keydown working");
        $(".page-link").attr("disabled",true).css("pointer-events","none");
        paused = false;
        startTime = Date.now() - elapsedTime;
        intervalId = setInterval(updateTime, 1000);
    }    
})

// Display and counting the stopwatch on the webpage
function updateTime(){
    elapsedTime = Date.now() - startTime;

    secs = Math.floor((elapsedTime / 1000) % 60);
    mins = Math.floor((elapsedTime / (1000 * 60)) % 60);
    hrs = Math.floor((elapsedTime / (1000 * 60 * 60)) % 60);
    
    secs = pad(secs);
    mins = pad(mins);
    hrs = pad(hrs);

    timeDisplay.textContent = `${hrs}:${mins}:${secs}`;

    function pad(unit){
        return (("0") + unit).length > 2 ? unit : "0" + unit;
    }
}

