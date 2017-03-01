import codecs
import os
import tweepy
import urllib2
import HTMLParser
from bs4 import BeautifulSoup
from triggering import tact
from secrets import *
from topia.termextract import tag
from time import gmtime, strftime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
tagger = tag.Tagger()
tagger.initialize()
hparser = HTMLParser.HTMLParser()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
tweets = api.user_timeline('VR Headlines')


def get_headlines():
    try:
        request = urllib2.Request("http://rss.nytimes.com/services/xml/rss/nyt/World.xml")
        response = urllib2.urlopen(request)
    except urllib2.URLError as e:
        print(e.reason)
    else:
        html = BeautifulSoup(response.read(), "html.parser")
        items = html.find_all('item')
        for item in items:
            headline = item.title.string
            h_split = headline.split()

            # don't want to use incomplete headlines
            if "..." in headline:
                continue

            # weed out all-caps headlines
            if count_caps(h_split) >= len(h_split) - 3:
                continue

            # skip offensive headlines
            if not tact(headline):
                continue

            # remove attribution string
            if "-" in headline:
                headline = headline.split("-")[:-1]
                headline = ' '.join(headline).strip()

            if process(headline):
                break
            else:
                continue


def tweet(headline):
    # check that we haven't tweeted this already
    for tweet in tweets:
        if headline == tweet.text:
            return False

    # Log tweet to file
    f = codecs.open(os.path.join(__location__, "vrheadlines.log"), 'a', encoding='utf=8')
    t = strftime("%d %b %Y %H:%M:%S:", gmtime())
    f.write("\n" + t + " " + headline)
    f.close()

    # tweet this ish
    api.update_status(headline)
    return True


def count_caps(headline):
    count = 0
    for word in headline:
        if word[0].isupper():
            count += 1
    return count


def is_replacable(word):
    """prefixes any noun starting with a lowercase letter"""
    if (word[1] == 'NN' or word[1] == 'NNS') and word[0][0].isalpha \
            and word[0][0].islower() and len(word[0]) > 1:
        return True
    else:
        return False


def process(headline):
    headline = hparser.unescape(headline).strip()
    tagged = tagger(headline)
    for i, word in enumerate(tagged):
        # avoid having two VRs in a row
        if is_replacable(word) and not is_replacable(tagged[i-1]):
            headline = headline.replace(" " + word[0], " VR " + word[0], 1)

    # don't tweet anything too long
    if len(headline) > 140:
        return False

    # don't tweet anything where a replacement hasn't been made
    if "VR" not in headline:
        return False

if __name__ == "__main__":
    get_headlines()