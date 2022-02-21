# The aim of this program is scrape data, or in this case, tweets from Twitter.
# In the aim of getting a better understanding of the impression or 'sentiment' users have of the implementation of restrictive Covid-19 policies. 


# Import the appropriate libraries - 

import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import sys
import re
import matplotlib.pyplot as plt   # Here we used the 'as' keyword to create an alias for the module we want to import. 
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # For this project, we are using both TextBlob and VADER for our sentiment analysis libraries. 




# Firstly, we need to earn access to the Twitter API through for this particular app(lication) -


# Twitter API credentials - consumer API key, the consumer API secret, access token and access token secret.   
# The below keys will likely be expired and will need to be regenerated via the Twitter Developer portal. 
Oauth1_consumer_key = "AVudPPS0nePRUgOAWNOOyQZB4"
oauth1_consumer_secret = "KeATWWKKjZYcJr9OExhMq1t2fKH35j5Z8hmPNwKOIg3EhwBHKv"
oauth1_access_token = "1454520951136194564-dXDgv1tI9EeRvMysAI1xpJxjpDW9hg"
oauth1_access_token_secret = "ByCcAp1zRDt2AuGCsu4astZtp78dBYDqjxQfh7G0dia7N"

# Creating an instance of tweepy's .AuthHandler class - 
authentication = tweepy.OAuthHandler(Oauth1_consumer_key, oauth1_consumer_secret)

# Setting the access token and access token secret - 
authentication.set_access_token(oauth1_access_token, oauth1_access_token_secret)

# Creating the API object, that accounts for our authentication information - 
# The Twitter API has a rate limit of 900 requests per 15 minutes, it would return an error for anything above this amount. 
# The 'wait_on_rate_limit' parameter asks whether or not to automatically wait for rate limits to replenish, in this case we set it to 'True' to avoid any errors.  
api = tweepy.API(authentication, wait_on_rate_limit= True)






# After authenticating our application, we can now use Tweepy, TextBlob and VADER to conduct sentiment analysis - 

# The below self-defined function will be used later to calculate the percentage of positive, negative and neutral Tweets we have in our sample.
# Where the 'part' paramater represents whatever category of sentiment we are interested in and the 'whole' parameter represents our total number of Tweets - NoOfTweets. 
def percentage(part,whole):
   return 100 * float(part)/float(whole)

# Recording the keyword(s) and number of Tweets being considered
keyword = input("Please enter keyword or hashtag to focus your search: ")
NoOfTweets = int(input ("Please enter how many tweets you want to analyse: "))

# Using tweepy to search and collect Tweets based on the predefined keyword(s) and number of Tweets we want to analyse - 
tweets = tweepy.Cursor(api.search_tweets, q = keyword).items(NoOfTweets) 
# Above we have defined what keyword(s) we want to analyse as well as the number of times this should be iterated. 
# The 'tweets' variable is just a list that contains all of the tweets from this iterative process of selecting related tweets. 

# Below are baseline counters that will be added to in order to keep track of the number of each tweet with different sentiment. 
# Where 'tweet_list' is all of the gathered text from tweets and all the others are a lists containing text from Tweets that have been sorted by sentiment -
positive = 0
negative = 0
neutral = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

# In the context of TextBlob, polarity indicates is a float in the range [-1-1], where 1 indicates a purely positive statement and -1 and purely negative statement.
# This varibale will not be placeholder to count the number of Tweets of whatever specification. 
# It will be measured for each iteration to keep account for the extent to which a tweet is positive or negative. 
polarity = 0

# A similar thing can be done for the subjectivity float score in the range of [0-1], 
# Where hypothetical a score of 0 represnts a purely objevtive statement and a score of 1 indicates a purely subjective statement. 
subjectivity = 0


for tweet in tweets: # For every Tweet in the list of 'NoOfTweets' Tweets that our API has scraped, 
   tweet_list.append(tweet.text) # Add the Tweet text data to tweet_list 

   # We can now make our first 'TextBlob', which is necessary to able to apply our methods for sentiment analysis. 
   # This is in the for loop, so each individual tweet will be treated as a TextBlob to be processed. 
   analysis = TextBlob(tweet.text) # This analysis variable will be needed to calculate your polarity value for each individual tweet. 
   
   # The polarity_scores method from the SentimentIntensityAnalyzer module, produces a dictionary of positive, negative, neutral and compound indexes.
   # It is very important to note, that VADER and Textblob, although fulfilling similar purposes, do so in slightly different ways. 
   # VADER produces individual scores for each interpretation, as well as an aggreagate compound score. 
   # While Textblob provides only a singular polarity score (that can be compared to the compound score produced by VADER).
   # As well as a subjectivity score, that aims to measure the degree of objectvity present in the statement can how opintionated it is. 
   # There are a few pros and cons for each library which are expanded on in the README file, but for the sake of whollsitic anaylsis, both will be used in this project. 
   
   # That in this case, describe the sentiment of the scraped tweet. 
   score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
   
   # We can now assign the scores associated with the dictionary keys produced, to new variables. 
   neg = score['neg']
   neu = score['neu']
   pos = score['pos']
   comp = score['compound']
   
   # +- is neccessary to add up all of the polarity score for whatever number of Tweets you analyse. 
   # This final score can later be divided by that same number of tweets and aggregated to produce an average polarity score for a specific topic. 
   polarity += analysis.sentiment.polarity 
   
   # A similar thing can be done for our subjectivity score - 
   subjectivity += analysis.sentiment.subjectivity 


# Depending on the scores produced, we can now sort each Tweet into distinct categories and aggregate overall sentiment - 
   if neg > pos: 
      negative += 1 
      negative_list.append(tweet)
            
   elif pos > neg: 
      positive += 1 
      positive_list.append(tweet)
      
   elif neg == pos: 
      neutral += 1 
      neutral_list.append(tweet)
   
   
  
positive_proportion = percentage(positive, NoOfTweets)
negative_proportion = percentage(negative, NoOfTweets)
neutral_proportion = percentage(neutral, NoOfTweets)
aggregated_polarity = polarity / NoOfTweets 
aggregated_subjectivity = subjectivity / NoOfTweets
   
  













