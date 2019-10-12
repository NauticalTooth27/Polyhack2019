import nltk
from nltk.corpus import stopwords
from collections import Counter
import math

doc1 = '''
Kevin McAleenan, the acting secretary of homeland security since April and the fourth person to serve in that post since the Trump presidency began, submitted his resignation to the White House on Friday, President Donald Trump announced Friday.
"Kevin McAleenan has done an outstanding job as Acting Secretary of Homeland Security. We have worked well together with Border Crossings being way down. Kevin now, after many years in Government, wants to spend more time with his family and go to the private sector," Trump said. "Congratulations Kevin, on a job well done! I will be announcing the new Acting Secretary next week. Many wonderful candidates!"
A source familiar with McAleenan's thinking tells CNN that the acting secretary felt he had accomplished all he could given the political realities of today -- specifically the unlikelihood that any legislative deal on immigration will happen in an election year. Moreover, with the numbers of undocumented immigrants apprehended or turned away at the border coming down for the fourth consecutive month -- 52,546 in September, a 65% drop from May -- the lack of crisis is dissuading members of Congress to act and compromise. McAleenan also has two young daughters and a wife with whom he wants to spend more time.
The announcement has been planned for weeks, sources close to McAleenan say, and has nothing to do with the Ukraine scandal in which Trump and several other Cabinet officials are currently enmeshed.

A source close to the process told CNN that White House officials tried to talk McAleenan out of resigning.
In a statement posted to Twitter, McAleenan thanked Trump for the opportunity to serve and department employees for their work. He said he would strive to ensure a smooth transition.
"With his support, over the last 6 months, we have made tremendous progress mitigating the border security and humanitarian crisis we faced this year, by reducing unlawful crossings, partnering with government in the region to counter human smugglers and address the causes of migration, and deploy additional border security resources," he said of Trump.
Sources close to McAleenan insist the decision has more to do with his feeling of having done all that he can do on the job as well as feeling the frustrations of someone who perceives his job to be non-partisan and does it from the perspective of a law enforcement officer.
McAleenan has also been in the position of working for a President who -- critics say --seems to see immigration in starkly political and often racist terms.
The President appointing hardliners to leadership positions in his department hasn't made his job any easier.
In an interview with The Washington Post published on October 1, McAleenan -- whom Trump never formally nominated for the Cabinet position -- said that while he controls his department, "What I don't have control over is the tone, the message, the public face and approach of the department in an increasingly polarized time. That's uncomfortable, as the accountable, senior figure."
Other acting figures in the department whose tone and tenor are more Trump-like -- acting commissioner of US Customs and Border Protection Mark Morgan and acting director of US Citizenship and Immigration Services Ken Cuccinelli -- have caused him difficulties, sources tell CNN, both by seemingly openly campaigning to replace him and by pushing rules that have seemed harsh to many in the public.
McAleenan found himself needing to respond to some of Cuccinelli's actions, such as ending consideration for most deportation deferrals for undocumented immigrants with serious medical conditions and ending automatic citizenship for children born abroad to certain US servicemembers and others.
Still, the acting secretary has been able to point to concrete accomplishments. Border apprehensions have declined significantly, numbers that included Central Americans and families crossing the border, representing the heart of the crisis. A source familiar with McAleenan's thinking says that he is proud of working with the governments of Mexico and the three Central American "Northern Triangle" countries -- El Salvador, Guatemala and Honduras -- to crack down on human smugglers and block caravans heading north.
"It felt like the layers are now in place to prevent a similar surge sparking this Fall," the source said.
A former DHS official said McAleenan understood the urgency of the situation.

"Starting with security partnerships first, McAleenan built a foundation of trust with the Northern Triangle countries that resulted in new bilateral agreements based on a shared commitment to confront irregular migration and eventually restore aid," the former official said. "The President's threat of tariffs on Mexico provided McAleenan with more opportunity to engage with an historically intractable partner on border security, resulting in a precipitous decline in apprehensions along the southern border."
McAleenan is also proud of having pushed DHS to declare unequivocally that white supremacists pose a growing threat to the American people, a statement the White House previously refused to make in as stark a way, the source close to the acting secretary said. "The El Paso shooting hit close to home," the source said, noting that six of those killed were family members of five agents and officers who work for the Department of Homeland Security.

'''

doc2 = '''
For more than a year, Joseph Roh illegally manufactured AR-15-style rifles in a warehouse south of Los Angeles.
His customers, more than two dozen of whom were legally prohibited from possessing a firearm, could push a button, pull a lever, and walk away a short time later with a fully assembled, untraceable semi-automatic weapon for about $1,000, according to court records.
Roh continued his black-market operation despite being warned in person by agents from the Bureau of Alcohol, Tobacco, Firearms and Explosives that he was breaking the law.
But five years after raiding his business and indicting him, federal authorities quietly cut a deal with Roh earlier this year and agreed to drop the charges.
Why?
The judge in the case had issued a tentative order that, in the eyes of prosecutors, threatened to upend the decades-old Gun Control Act and "seriously undermine the ATF's ability to trace and regulate firearms nationwide."

A case once touted by prosecutors as a crackdown on an illicit firearms factory was suddenly seen as having the potential to pave the way to unfettered access to one of the most demonized guns in America.
Federal authorities preferred to let Roh go free rather than have the ruling become final and potentially create case law that could have a crippling effect on the enforcement of gun laws, several sources familiar with the matter told CNN. Each requested anonymity due to the sensitive nature of the case and its possible implications.
'''

doc3 = '''
It amounted to a challenging end of a challenging week for Trump, who remains consumed by an impeachment crisis that is clouding his presidency.
Within moments of each other, a career diplomat began painting a damning portrait of the President's foreign policy to lawmakers just as Trump lost his appeal in a federal appeals court to stop a House subpoena of his tax documents, which he's guarded fiercely since refusing to make them public as a candidate.
Then, in rapid succession, judges in New York, Texas, Washington state and California sided against Trump administration initiatives meant to limit immigrants from entering the country -- both through a physical barrier and by raising the requirements on migrants seeking legal status.

Friday night, the man in charge of executing much of Trump's immigration agenda, acting Homeland Security Secretary Kevin McAleenan, submitted his resignation to the President as the legal setbacks mounted. Long in the works, and by all accounts unrelated to the court decisions or the impeachment crisis, the move nonetheless fueled a sense of an administration in flux. McAleenan was the fourth person to serve in that post since the Trump presidency began.
All of the court cases will be appealed. But the rulings added to the sense of Trump's worsening legal fortunes, and Democratic investigations into his finances and foreign activity seemed to gain steam.
A silver lining came in the afternoon, when Trump announced a "phase one" trade agreement with China that he hopes will signal the beginning of the end of a withering trade war. News of the emerging deal sent stocks soaring, even as the President acknowledged it still requires "papering." '''

NUM_KEYWORDS = 5

# keywordify
# Takes list of N strings for documents
# Returns 2D, NxM list of string keywords; match up to articles
def keywordify(documents) :
    num_docs = len(documents)

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    word_tokenizer = nltk.tokenize.punkt.PunktLanguageVars()
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    term_freqs = [None] * num_docs
    all_freqs = Counter()
    keywords = [None] * num_docs

    # Clean all docs
    for doc_idx in range(num_docs) :
        sent_tokens = tokenizer.tokenize(documents[doc_idx].strip())
        word_tokens = [word_tokenizer.word_tokenize(sent) for sent in sent_tokens]
        tokens = []
        for wt in word_tokens :
            tokens.extend(wt)
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
        term_freqs[doc_idx] = Counter(tokens)
        all_freqs += term_freqs[doc_idx]

    idf = {}
    for term in all_freqs :
        idf[term] = math.log(num_docs / len([doc_idx for doc_idx in range(num_docs) if term_freqs[doc_idx][term] > 0]))

    for doc_idx in range(num_docs) :
        tfidf = {}
        for term in term_freqs[doc_idx] :
            tfidf[term] = term_freqs[doc_idx][term] * idf[term]
        try :
            top_keys = sorted(tfidf, key=tfidf.get, reverse=True)[:NUM_KEYWORDS]
            keywords[doc_idx] = {k:tfidf[k] for k in top_keys}
        except :
            print("Error in except, keywordify 1")
            keywords[doc_idx] = tfidf

    return keywords
