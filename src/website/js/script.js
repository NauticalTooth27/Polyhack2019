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
var articles = [
    new ArticleInfo("Yeet","CNN","10/11/19","Climate Change","Yeet the Wheat","Good",LEFT),
    new ArticleInfo("Skree","Fox News","10/11/19","Climate Change","Don't Yeet the Wheat","Bad",RIGHT)
];

function printArticle(leaning) {
    var article = getNextArticle(leaning);
    if(article == null) {
        document.write("<br>");
        return;
    }

    document.write("<button onclick = 'popupArticle('popuparticle.html',article);'>"
    + article.title + " | " + article.publisher + "</button>");
    return;
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
    for (var i = 0; i <= articles.length; i++) {
        if (articles[i] != null && articles[i].leaning == leaning) {
            var temp = articles[i];
            articles[i] = null;
            return temp;
        }
    }
    return null;
}

function popupArticle(url,article){
    console.log("Skree");
    settings = 'height='+500+',width='+500+',top='+100+',left='+100+',scrollbars=no,resizable';
    popupWindow = window.open(url,article.title,settings);
    printArticleSmart(popupWindow,article);
}
