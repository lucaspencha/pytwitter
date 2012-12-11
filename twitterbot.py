#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import random
import sys
import time

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="*****"
consumer_secret="*****"
# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="*****"
access_token_secret="*****"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
me = api.me().screen_name

#Insert @%s when you want to insert a specific username

TEMPLATES = [
	'message 1',
	'message 2',
  	'message 3',
 	'message 4',
  	'message 5'
]

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        """ Load the data into json and then return the username as the
        name variable
        """
        data_string = json.loads(data)
        name = data_string["user"]["screen_name"]
        user_id = data_string["user"]["id_str"]
        # Call the timer, this sets the delay beween actions.
        timer()
        # Call the counter
        count()
        # This is for replying to people
        if choice == 1:
            # Print the tweet that we are about to reply to
            print data_string["text"]
            # Reply to it using the templates function at the top
            api.update_status(TEMPLATES[random.randint(0,4)] %(name), data_string["id"])
            return True
        # This is for following new people
        elif choice == 2:
            # Try to follow them, if it failes we are already following
            im_following = api.friends_ids(me)
            if str(user_id) in im_following:
                print("Already following: " + name)
                return True
            api.create_friendship(name)
            print("Now following: " + name)
            return True
            return True
    def on_error(self, status):
        return True

# This is for unfollowing those bastards who never follow back.
def clean_followers():
    # Call the timer
    timer()
    # Get a list of all the people I'm following
    im_following = api.friends_ids(me)
    for i in range(len(im_following)):
        if count():
            # Check to see if they are following me back
            if api.exists_friendship(im_following[i], me)==False:
                # They are not so I need to unfollow them.
                api.destroy_friendship(im_following[i])
                print("Unfollowed " + str(im_following[i]))
    print im_following
    main_menu()
    
def clear_followers():
    # Call the timer
    timer()
    # Get a list of all the people I'm following
    im_following = api.friends_ids(me)
    for i in range(len(im_following)):
        if count():
            # Unfollow them
            api.destroy_friendship(im_following[i])
            print("Unfollowed " + str(im_following[i]))
    print im_following
    main_menu()
    
def timer():
    global tweet_timer
    """ Here is the timer that adds plus or minus seconds to make the bot
    seem more random
    """        
    time.sleep(random.randint(tweet_timer, tweet_timer+1))
    return True

def count():
    global counter
    if counter == 0:
        print("Limit reached")
        main_menu()
    counter = counter -1
    print counter
    return True

def main():
    l = StdOutListener()
    stream = Stream(auth, l)	
    stream.filter(track=[choice_keyword])

def main_menu():
    global choice
    global choice_keyword
    global counter
    global tweet_timer
    global twitter_followers
    if api.verify_credentials()==False:
        print("Your login has failed, please check your keys")
        pass
        #sys.exit()
    print("Menu")
    print("You have "+ str(api.rate_limit_status())+ " api calls left in this hour.")
    print("Please make a selection")
    print("1. Reply to tweets")
    print("2. Follow People")
    print("3. Unfollow people not following back.")
    print("4. Unfollow everyone.")
    choice = int(raw_input("Please enter your selection: "))
    counter = int(raw_input("How many times would you like to do this?: "))-1
    tweet_timer = int(raw_input("Enter the time in seconds between actions: "))
    if choice == 3:
        clean_followers()
    if choice == 3:
        clear_followers()
    choice_keyword = str(raw_input("Please enter your keyword: "))
    main()  


if __name__ == '__main__':
    main_menu()

    
