function ArticleInfo(title, publisher, date, topic, description, sentiment,leaning) {
    this.title = title;
    this.publisher = publisher;
    this.date = date;
    this.topic = topic;
    this.description = description;
    this.sentiment = sentiment;
    this.leaning = leaning;
}

var popupWindow = null;

const LEFT = 0;
const CENTER = 1;
const RIGHT = 2;
var articles = [];

readInArticle("Yeet","CNN","10/11/19","Climate Change","Yeet the Wheat","Good",LEFT);
readInArticle("Skree","Fox News","10/11/19","Climate Change","Don't Yeet the Wheat","Bad",RIGHT);

var i = 0;
function printArticle(leaning) {
    var article = getNextArticle(leaning);
    if(article == null) {
        document.write("<br>");
        return;
    }
    document.write("<button onclick = 'createPopupArticle('popuparticle.html',"+i+");'>" + article.title + " | " +
                    article.publisher + "</button>");
    return;
}

function readInArticle(title, publisher, date, topic, description, sentiment,leaning) {
    articles.push(new ArticleInfo(title, publisher, date, topic, description, sentiment,leaning));
}

function printArticleSmart(printWindow,article) {
    if(article == null) {
        printWindow.document.write("<br>");
        return;
    }

    printWindow.document.write(article.title + "<br>" + article.publisher + "<br>" +
                    article.date + " | " + article.topic + "<br>" +
                    article.description + "<br>" + article.sentiment);
    return;
}

function getNextArticle(leaning) {
    for (i = i; i <= articles.length; i++) {
        if (articles[i] != null && articles[i].leaning == leaning) {
            var temp = articles[i];
            articles[i] = null;
            return temp;
        }
    }
    return null;
}

function popupArticle(url,numarticle){
    article = articles[numarticle];
    console.log("Skree");
    settings = 'height='+500+',width='+500+',top='+100+',left='+100+',scrollbars=no,resizable';
    popupWindow = window.open(url,article.title,settings);
    printArticleSmart(popupWindow,article);
}


function scrollingUp(speed) {
  var elem1 = document.getElementById("animate");
  var elem2 = document.getElementById("animate2");
  var elem3 = document.getElementById("animate3");
  var elem4 = document.getElementById("animate4");
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
           // count++;
           // elem1.style.left += ((count * 30) % w) + 'px';
           // elem2.style.left += ((count * 30) % w) + 'px';
            //elem3.style.left += ((count * 30) % w) + 'px';
           // elem4.style.left += ((count * 30) % w) + 'px';
        pos = -30;
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

