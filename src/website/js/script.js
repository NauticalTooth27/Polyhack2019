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
var currIndex = 1;

function printArticle(leaning) {
    console.log("yeet");
    if(currIndex == -1) {
        document.write("<br>");
        return;
    }
    if(leaning == LEFT) {
        document.write("l");
    } else if(leaning == CENTER) {
        document.write("c");
    } else if(leaning == RIGHT) {
        document.write("r");
    }
    return;
}
