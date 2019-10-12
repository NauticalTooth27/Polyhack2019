function scrollingUp(speed) {
  var elem1 = document.getElementById("red1");
  var elem2 = document.getElementById("blue1");
  var elem3 = document.getElementById("red2");
  var elem4 = document.getElementById("blue2");
  var count = 0;
  var pos = 0;
  var posrev = window.innerHeight;
  var id = setInterval(frame, speed);
  function frame () {
    var w = 0.0
    var w = window.innerWidth;
    w = w / 10 * 3;
    var h = window.innerHeight;
    if (pos == h) {
            count++;
            elem1.style.left = "75%";
           // elem2.style.left += ((count * 30) % w) + 'px';
            //elem3.style.left += ((count * 30) % w) + 'px';
           // elem4.style.left += ((count * 30) % w) + 'px';
        pos = -400;
        posrev = window.innerHeight;
    } else {
      pos++;
      posrev--;
      elem1.style.top = pos + 'px';
      elem2.style.top = posrev + 'px';
      elem3.style.top = pos + 'px';
      elem4.style.top = posrev + 'px';
    }
  }
}
