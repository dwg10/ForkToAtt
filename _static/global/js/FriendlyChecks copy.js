/* function startTimer(duration, display) {
  var timer = duration, minutes, seconds;
  setInterval(function () {
      minutes = parseInt(timer / 60, 10);
      seconds = parseInt(timer % 60, 10);

      // minutes = minutes < 10 ? "0" + minutes : minutes;
      // seconds = seconds < 10 ? "0" + seconds : seconds;

      // display.text(minutes + ":" + seconds);
      display.text(seconds);

      if (--timer < 0) {
          timer = duration;
      }
  }, seconds * 1000);
} */

jQuery(function ($) {
  var fifteenSec = 60 * 0.05,
      display = $('#time');
  startTimer(fifteenSec, display);
  setTimeout(function(){
    window.location.href = 'task.html';
  }, 3000);
});