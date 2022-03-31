import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items

def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    items = loadkeys(twitter_auth_filename)
    twitter_auth_filename = items[0].split(',')
    auth = tweepy.OAuthHandler(twitter_auth_filename[0],twitter_auth_filename[1])
    auth.set_access_token(twitter_auth_filename[2],twitter_auth_filename[3])
    api = tweepy.API(auth)
    return api

def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    analysis =SentimentIntensityAnalyzer()
    mylist=[]
    for status in tweepy.Cursor(api.user_timeline, id=name).items(100):
        mydict={}
        mydict['id'] = status.id
        mydict['created'] = status.created_at
        mydict['retweeted'] = status.retweet_count
        mydict['text'] = status.text
        mydict['hashtags'] = status.entities['hashtags']
        if status.entities['urls'] == []:
            mydict['urls'] = status.entities['urls']
        else:
            mydict['urls'] = status.entities['urls'][0]['url']
        if status.entities['user_mentions'] == []:
            mydict['mentions'] = status.entities['user_mentions']
        else:
            mydict['mentions'] = status.entities['user_mentions'][0]['screen_name']
        mydict['score'] = analysis.polarity_scores(status.text)['compound']
        mylist.append(mydict)
    return_dic = {"user":name, "count":api.get_user(screen_name = name).statuses_count,"tweets":mylist}
    return return_dic   
           

def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get the list of User objects back from friends();
    get a maximum of 100 results. Pull the appropriate values from
    the User objects and put them into a dictionary for each friend.
    """
    mylist=[]
    for friend in tweepy.Cursor(api.get_friends, screen_name=name).items(100):
        mydict={}
        mydict['name']=friend.name
        mydict['screen_name']=friend.screen_name
        mydict['followers']=friend.followers_count
        mydict['created']=str(friend.created_at.date())
        mydict['image']=friend.profile_image_url_https
        mylist.append(mydict)
    return mylist
