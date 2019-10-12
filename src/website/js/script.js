function ArticleInfo(title, publisher, date, topic, description, sentiment,leaning) {
    this.title = title;
    this.publisher = publisher;
    this.date = date;
    this.topic = topic;
    this.description = description;
    this.sentiment = sentiment;
    this.leaning = leaning;
}

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

    document.write(article.title + " | " + article.publisher + "<br>" +
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
