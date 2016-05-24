#Creating Twitter Clique

import twitter
import time
import sys
import json
import ast

#TODO: A lot of repeated code in the functions. Find a way to refactor.

BAD_USER_LIMIT = 50
SLEEP_TIME = 300

newToken = 1
capTemp = 0
newToken0 = 1
capTemp0 = 0
newToken1 = 1
capTemp1 = 0
newTokenT = 1
capTempT = 0

friend_index = 0 # token list index
user_index = 0 # token list index
followers_index = 0 # token list index 
timeline_index = 0 # token list index

#Bad accounts counter for each type of twitter request
bad_user_counter_tm = 0
bad_user_counter_ff = 0
bad_user_counter_u = 0
"""
#506 Users Database Connection
db = MySQLdb.connect(host="localhost", user="alireza", passwd="", db="test")
cursor = db.cursor()
cursor.execute("SELECT DISTINCT oauth_token, oauth_secret FROM users")
numrows = int(cursor.rowcount)

userlist = []
results = cursor.fetchall()

for row in results:
    userlist.append([row[0], row[1]])

with open("userlist.json", "wb") as f:
    f.write(json.dumps(userlist))
"""

with open("userlist.json", "rb") as f:
    userlist = json.loads(f.read())

#Unlock api
consumer_key = "gRS5uF1jQFqccGxi2F5JTQ"
consumer_secret = "ZiL9PYgbwDm2kjJQJCIGTWsqwJSta2m1aRe7N61fw"

access_token = userlist[friend_index][0]
access_token_secret = userlist[friend_index][1]

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)

#Remove blocked users, or users not having full capacity
if "-usercheck" in sys.argv:
    #User check
    remove_count = 0

    for user in userlist:
        access_token = user[0]
        access_token_secret = user[1]
        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            capacity = api.GetRateLimitStatus()
            formatted = capacity['resources']['friends']['/friends/ids']['remaining']
            if formatted < 15:
                userlist.remove(user)
                remove_count += 1
        except:
            userlist.remove(user)
            remove_count += 1
    
    print "Info: removed ", remove_count, " users."

MAX_Token_NUM = len(userlist)

#Followers
def get_user_followers(userid, only_id=True, page_id=-1):
    global followers_index
    global api
    global newToken1
    global capTemp1
    global bad_user_counter_ff

    if newToken1 == 1:
        limit = api.GetRateLimitStatus()
        if only_id:
            cap = limit['resources']['followers']['/followers/ids']['remaining']
        else:
            cap = limit['resources']['followers']['/followers/list']['remaining']

            
        capTemp1 = cap
        newToken1 = 0

    wait_time = 1
    first_time = True    
    
    while capTemp1 <= 2:
        if not first_time:
            time.sleep(wait_time)
            wait_time *= 1.5
        
        first_time = False

        followers_index = (followers_index + 1) % MAX_Token_NUM
    
        access_token = userlist[followers_index][0]
        access_token_secret = userlist[followers_index][1]

        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            limit = api.GetRateLimitStatus()
            
            if only_id:
                cap = limit['resources']['followers']['/followers/ids']['remaining']
            else:
                cap = limit['resources']['followers']['/followers/list']['remaining']
            
            capTemp1 = cap

            if capTemp1 != 15:
                bad_user_counter_ff += 1

                if bad_user_counter_ff > BAD_USER_LIMIT:
                    print "Starting sleep"
                    time.sleep(SLEEP_TIME)
                    print "Finished sleep"
                    bad_user_counter_ff = 0

        except Exception as e:
            print "Api call : "
            print e
            if hasattr(e, u'message') and isinstance(e.message, list):
                error = e.message[0][u'message']
            else:
                error = e.message
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp1 = 0

    try:  
        if only_id:
            followers = api.GetFollowerIDs(user_id=userid)#, total_count=5000)
        else:
            followers = api.GetFollowers(user_id=userid, cursor=page_id)

        capTemp1 = capTemp1 - 1
        #limit = api.GetRateLimitStatus()
        #if only_id:
            #capTemp1 = limit['resources']['followers']['/followers/ids']['remaining']
        #else:
            #capTemp1 = limit['resources']['followers']['/followers/list']['remaining']
    except Exception as e:
        if hasattr(e, u'message') and isinstance(e.message, list):
            error = e.message[0][u'message']
        else:
            error = e.message

        if error == u'Sorry, that page does not exist':
            capTemp1 = capTemp1 - 1 
            return [] #User does not exist anymore
        
        if "Not authorized" in error:
            print "User " + str(userid) + " is protected."
            capTemp1 = capTemp1 - 1
            return []
        else:
            print "Api call : "
            print e
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp1 = 0

        return None
    
    return followers


#Friends
def get_user_friends(userid, only_id=True, page_id=-1):
    global friend_index
    global api
    global newToken0
    global capTemp0
    global bad_user_counter_ff

    if newToken0 == 1:
        limit = api.GetRateLimitStatus()
        if only_id:
            cap = limit['resources']['friends']['/friends/ids']['remaining']
        else:
            cap = limit['resources']['friends']['/friends/list']['remaining']
        
        capTemp0 = cap
        newToken0 = 0

    wait_time = 1
    first_time = True    

    while capTemp0 <= 2:
        if not first_time:
            time.sleep(wait_time)
            wait_time *= 1.5
        
        first_time = False
        friend_index = (friend_index + 1) % MAX_Token_NUM
    
        access_token = userlist[friend_index][0]
        access_token_secret = userlist[friend_index][1]

        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            limit = api.GetRateLimitStatus()
            
            if only_id:
                cap = limit['resources']['friends']['/friends/ids']['remaining']
            else:
                cap = limit['resources']['friends']['/friends/list']['remaining']

            capTemp0 = cap

            if capTemp0 != 15:
                bad_user_counter_ff += 1

                if bad_user_counter_ff > BAD_USER_LIMIT:
                    print "Starting sleep"
                    time.sleep(SLEEP_TIME)
                    print "Finished sleep"
                    bad_user_counter_ff = 0

        except Exception as e:
            print "Api call : "
            print e
            
            if hasattr(e, u'message') and isinstance(e.message, list):
                error = e.message[0][u'message']
            else:
                error = e.message

            if e.message[0][u'message'] == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp0 = 0

    try:  
        if only_id:
            friends = api.GetFriendIDs(user_id=userid)
        else:
            #TODO: Find out why he sleeps here. Is the limit fetched the wrong one? Why aren't we getting an error/exception?
            friends = api.GetFriends(user_id=userid, cursor=page_id)

        capTemp0 = capTemp0 - 1
        #limit = api.GetRateLimitStatus()
        
        #if only_id:
            #capTemp0 = limit['resources']['friends']['/friends/ids']['remaining']
        #else:
            #capTemp0 = limit['resources']['friends']['/friends/list']['remaining']
    except Exception as e:
        if hasattr(e, u'message') and isinstance(e.message, list):
            error = e.message[0][u'message']
        else:
            error = e.message

        if error == u'Sorry, that page does not exist':
            capTemp0 = capTemp0 - 1
            return None #User does not exist anymore
        
        if "Not authorized" in error:
            print "User " + str(userid) + " is protected."
            capTemp0 = capTemp0 - 1
            return []
        else:
            print "Api call : "
            print e
            print "While friends: limit is " + str(capTemp0)
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp0 = 0

        return None
    
    return friends


def get_user(userid):
    global user_index
    global api
    global newToken
    global capTemp
    global bad_user_counter_u

    cap_got = False
    cap = 0
    
    if newToken == 1: 
        limit = api.GetRateLimitStatus()
        cap = limit['resources']['users']['/users/show/:id']['remaining']
        capTemp = cap
        newToken = 0
    
    wait_time = 1
    first_time = True
    
    while capTemp <= 2:
        if not first_time:
            time.sleep(wait_time)
            wait_time *= 1.5
        
        first_time = False
        user_index = (user_index + 1) % MAX_Token_NUM
        access_token = userlist[user_index][0]
        access_token_secret = userlist[user_index][1]
        
        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            limit = api.GetRateLimitStatus()
            cap = limit['resources']['users']['/users/show/:id']['remaining']
            capTemp = cap

            if capTemp != 15:
                bad_user_counter_u += 1

                if bad_user_counter_u > BAD_USER_LIMIT:
                    print "Starting sleep"
                    time.sleep(SLEEP_TIME)
                    print "Finished sleep"
                    bad_user_counter_u = 0
        except Exception as e:
            print "Api call : "
            print e
            
            if hasattr(e, u'message') and isinstance(e.message, list):
                error = e.message[0][u'message']
            else:
                error = e.message
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp = 0

    capTemp = capTemp - 1
    
    try:    
        user = api.GetUser(userid)
    except Exception as e:
        if hasattr(e, u'message') and isinstance(e.message, list):
            error = e.message[0][u'message']
        else:
            error = e.message

        if error == u'Sorry, that page does not exist':
            capTemp = capTemp - 1
            return [[]] #User does not exist anymore
        
        if "Not authorized" in error:
            print "User " + str(userid) + " is not authorized."
            capTemp = capTemp - 1
        else:
            print "While user: limit is " + str(capTemp)
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTemp = 0
        
        return None

    return user


#UserTimeline
def get_user_timeline(userid, max_idd):
    global timeline_index
    global api
    global newTokenT
    global capTempT
    global bad_user_counter_tm

    cap_got = False
    cap = 0
    
    if newTokenT == 1:
        limit = api.GetRateLimitStatus()
        cap = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
        capTempT = cap
        newTokenT = 0

    wait_time = 1
    first_time = True
    while capTempT <= 5:
        if not first_time:
            time.sleep(wait_time)
            wait_time *= 1.5
            
        first_time = False
        timeline_index = (timeline_index + 1) % MAX_Token_NUM
        #print "timeline_index=",timeline_index
        access_token = userlist[timeline_index][0]
        access_token_secret = userlist[timeline_index][1]
        
        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            limit = api.GetRateLimitStatus()
            cap = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
            capTempT = cap

            if capTempT != 15:
                bad_user_counter_tm += 1

                if bad_user_counter_tm > BAD_USER_LIMIT:
                    print "Starting sleep"
                    time.sleep(SLEEP_TIME)
                    print "Finished sleep"
                    bad_user_counter_tm = 0
        except Exception as e:
            print "Api call : "
            print e
            
            if e.message[0][u'message'] == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTempT = 0
            
    capTempT = capTempT - 1
    try:
        if max_idd != -1:
            timeline = api.GetUserTimeline(userid, max_id=max_idd, count=180)
        else:
            timeline = api.GetUserTimeline(userid, count=180)
    except Exception as e:
        if hasattr(e, u'message') and isinstance(e.message, list):
            error = e.message[0][u'message']
        else:
            error = e.message

        if error == u'Sorry, that page does not exist.':
            capTempT = capTempT - 1
            return [] #User does not exist anymore
            
        if "Not authorized" in error:
            print "User " + str(userid) + " is protected."
            capTempT = capTempT - 1
            return []
        else:
            print "Api call : "
            print e
            
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTempT = 0
        
        return None
    
    return timeline


#Get sample of tweets
def get_sample():
    global user_index
    global api
    global newToken
    global capTempT

    cap = 0
    
    if newToken == 1: 
        limit = api.GetRateLimitStatus()
        #TODO: Pretty sure this isn't the right resource, but since this is never used entirely it isn't critical
        cap = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
        capTempT = cap
        newToken = 0
    
    wait_time = 1
    first_time = True
    
    while capTempT <= 5:
        if not first_time:
            time.sleep(wait_time)
            wait_time *= 1.5
        
        first_time = False
        user_index = (user_index + 1) % MAX_Token_NUM
        access_token = userlist[user_index][0]
        access_token_secret = userlist[user_index][1]
        
        try:
            api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
            limit = api.GetRateLimitStatus()
            cap = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
            capTempT = cap
        except Exception as e:
            print "Api call : "
            print e
            
            if e.message[0][u'message'] == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTempT = 0

    capTempT = capTempT - 1
    
    try:    
        sample = api.GetStreamSample()
    except Exception as e:
        if hasattr(e, u'message') and isinstance(e.message, list):
            error = e.message[0][u'message']
        else:
            error = e.message

        if error == u'Sorry, that page does not exist':
            capTempT = capTempT - 1
            return [[]] #User does not exist anymore
        
        if "Not authorized" in error:
            print "User " + str(userid) + " is not authorized."
            capTempT = capTempT - 1
        else:
            if error == u'Rate limit exceeded':
                limit = api.GetRateLimitStatus()
                with open("logs.txt", "a") as f:
                    f.write(json.dumps(limit))
                    f.write("\n")
            
            capTempT = 0
        
        return []

    return sample


def get_sleep_time(resource):
    global api

    return api.GetSleepTime(resource)
