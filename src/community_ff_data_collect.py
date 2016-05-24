import random
import twitter_api
import ast
import sys
import os
import time
import json

MAX_FF = 2000
SAMPLE_FILE_PATH = 'community/user_sample.json'
user_sample = []

def create_user_sample():
    sample_stream = twitter_api.get_sample()

    for sample in sample_stream:
        if len(user_sample) > 1000:
            break
        
        if len(sample) > 1:
            user = sample[u'user']
            user_sample.append(user)

    with open(SAMPLE_FILE_PATH, "wb") as f:
        f.write(json.dumps(user_sample))


#This is for a depth of 2 instead of 1
def friend_loop(user_id):
    tmp_friends = twitter_api.get_user_friends(user_id, True)
    page_count = 0
    friends = []
    print len(tmp_friends)

    while len(tmp_friends) == 200: 
        friends += tmp_friends
        tmp_friends = twitter_api.get_user_friends(user_id, False, page_count)
        page_count += 1

    friends += tmp_friends

    return friends


#This is for a depth of 2 instead of 1
def follower_loop(user_id):
    tmp_followers = twitter_api.get_user_followers(user_id, False)
    page_count = 0
    followers = []
    print len(tmp_followers)

    while len(tmp_followers) == 200: 
        followers += tmp_followers
        tmp_followers = twitter_api.get_user_followers(user_id, False, page_count)
        page_count += 1

    followers += tmp_followers

    return followers


def get_user_ff():
    for user in user_sample:
        friends_c = int(user[u'friends_count'])
        followers_c = int(user[u'followers_count'])
        
        #A too high count of followers or friends indicate a celebrity
        if followers_c > MAX_FF or friends_c > MAX_FF:
            continue

        if followers_c == 0 and friends_c == 0:
            continue
        
        friends_dict = {}
        followers_dict = {}
        user_id = user[u'id_str']

        if user_id in os.listdir("community/english/"):
            continue

        if user[u'protected']:
            continue

        if not user[u'lang'].startswith("en"):
            continue
        
        start = time.time()
        print "doing user : " + user_id
        print "Counts: " + str(friends_c) + " friends, " + str(followers_c) + " followers."

        main_friends = twitter_api.get_user_friends(user_id, True)
        main_followers = twitter_api.get_user_followers(user_id, True)

        tries = 0
        while (main_friends == None or main_followers == None) and tries < 3:
            time.sleep(60)
            main_friends = twitter_api.get_user_friends(user_id, True)
            main_followers = twitter_api.get_user_followers(user_id, True)
            tries += 1
        
        if not main_friends or not main_followers:
            continue

        user = twitter_api.get_user(user_id)
        friends_dict[user.AsJsonString()] = main_friends
        followers_dict[user.AsJsonString()] = main_followers
        
        for friend in main_friends:
            user = twitter_api.get_user(friend)
            if not user:
                continue

            #A too high count of followers or friends indicate a celebrity
            if user and not user.protected  and (user.GetFriendsCount() > MAX_FF or user.GetFollowersCount() > MAX_FF):
                continue
            
            friends = twitter_api.get_user_friends(friend, True)
            followers = twitter_api.get_user_followers(friend, True)
            tries = 0

            while (friends == None or followers == None) and tries < 3:
                time.sleep(60)
                friends = twitter_api.get_user_friends(friend, True)
                followers = twitter_api.get_user_followers(friend, True)
                tries += 1

            if not friends or not followers:
                continue
            
            friends_dict[user.AsJsonString()] = friends
            followers_dict[user.AsJsonString()] = followers

        for follower in main_followers:
            user = twitter_api.get_user(follower)
            if not user:
                continue
            
            #A too high count of followers or friends indicate a celebrity
            if user and not user.protected and (user.GetFriendsCount() > MAX_FF or user.GetFollowersCount() > MAX_FF):
                continue
            
            friends = twitter_api.get_user_friends(follower, True)
            followers = twitter_api.get_user_followers(follower, True)
            tries = 0

            while (friends == None or followers == None) and tries < 3:
                time.sleep(60)
                friends = twitter_api.get_user_friends(follower, True)
                followers = twitter_api.get_user_followers(follower, True)
                tries += 1

            if not friends or not followers:
                continue
            
            friends_dict[user.AsJsonString()] = friends
            followers_dict[user.AsJsonString()] = followers

        os.mkdir("community/english/" + user_id)
        with open("community/english/" + user_id + "/friends.json", "wb") as f:
            f.write(json.dumps(friends_dict))
        
        with open("community/english/" + user_id + "/followers.json", "wb") as f:
            f.write(json.dumps(followers_dict))

        end = time.time()
        print "Elapsed time: " + str(end - start)


if __name__ == "__main__":
    if "-sample" in sys.argv:
        create_user_sample()
    else:
        with open(SAMPLE_FILE_PATH, "rb") as f:
            user_sample = json.loads(f.read())

    if "-ff" in sys.argv:
        get_user_ff()

    print "done"
