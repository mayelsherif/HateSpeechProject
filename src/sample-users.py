import pandas as pd
import csv
import os
import random

'''
	Randomly sample n users from the 1% Twitter dataset, 
	where n equals the number of users in the hate speech dataset
'''
maindir = "../../../twitter-data/"
outdir = "../results/"
colnames = ['timestamp', 'tid', 'tsource', 'uid', 'user_name', 'user_screen_name', 'user_account_start', 
'replytostatus', 'replytouser', 'oid', 'ouid', 'ufollowcount', 'ufriendcount', 'ufavecount', 
'uretweetcount', 'ustatuscount', 'user_listedcount', 'user_loc', 'user_timezone', 
'user_geoenabled', 'user_url ', 'user_profile_img_url', 'user_default_img_bool', 
'user_verified', 'user_description', 'lat', 'lng', 'mentions', 'hashtags', 'urls', 'media', 
'timestamp-otimestamp', 'otimestamp', 'oufollowcount', 'oufriendcount', 'oufavecount', 
'oustatuscount', 'olat', 'olng', 'tex'] #

def get_num_unique_hate_users(dir):
    print "Counting number of unique users in hate speech dataset..."
    unique_users = set()
    files = os.listdir(maindir + dir)
    for file in files:
        if file not in ['2016_Jan_Feb_i_hate.tsv', '2017_Jan_Feb_i_hate.tsv', '2016_Jan_Feb_ht.tsv', '2017_Jan_Feb_ht.tsv']:
            df = pd.read_csv(open(maindir + dir + file,'rU'), names=colnames, header=None, delimiter='\t')
            tmp = df.uid.unique()
            unique_users.update(tmp)
    print len(unique_users)
    return(unique_users)
    #35808, 35044

def get_unique_users(file):
    print "Counting number of unique users in general dataset..."
    userids = set()
    with open(file,'r') as infile:
        for line in infile:
            try:
                items = line.split('\t')
                # print items
                if len(items)>0:
                    userid = items[3]
                    # print userid
                    userids.add(userid)
            except Exception:
                # print "Error..."
                pass
    print file, len(userids)
    return userids

def sample_users():
    dirs = {'2016_Jan_Feb_dataset/':29340, '2017_Jan_Feb_dataset/':29365}
    for dir in dirs:
        print dir
        # num_hate_users = get_num_unique_hate_users(dir)
        num_hate_users = int(dirs[dir])
        file = dir.replace('dataset/', 'general.tsv')
        # number of tweets: [240214340, 184701980]
        outfilename = outdir + dir.replace('dataset/', 'user_sample.tsv')
        # userids = get_unique_users(maindir + file)
        num_userids = 38790147

        prob = num_hate_users/ float(num_userids)
        print prob
        print "Sampling users from general dataset..."
        rnd_users = set()
        with open(maindir + file,'rU') as infile, open(outfilename, "w") as outfile:
            for line in infile:
                try:
                    items = line.split('\t')
                    # print items
                    # print len(items)
                    if len(items)>0:
                        userid = items[3]                        
                        # print userid
                        if userid not in rnd_users:
                            rnd = random.random()
                            print rnd
                            if rnd < prob:
                                 outfile.write(line)
                                 rnd_users.add(userid)

                except Exception:
                    # print "Error..."
                    pass


sample_users()

# 2016_Jan_Feb_dataset/
# 2016_Jan_Feb_gender.tsv 31963 26847
# 2016_Jan_Feb_class.tsv 2436 2219
# 2016_Jan_Feb_nationality.tsv 82 56
# 2016_Jan_Feb_ht.tsv 1927 1567
# 2016_Jan_Feb_ethnicity.tsv 4097 3767
# 2016_Jan_Feb_religion.tsv 67 42
# 2016_Jan_Feb_sexorient.tsv 1402 1310
# 29340
# 2017_Jan_Feb_dataset/
# 2017_Jan_Feb_ht.tsv 722 696
# 2017_Jan_Feb_gender.tsv 28053 25336
# 2017_Jan_Feb_ethnicity.tsv 5150 4996
# 2017_Jan_Feb_class.tsv 2937 2836
# 2017_Jan_Feb_religion.tsv 25 24
# 2017_Jan_Feb_nationality.tsv 30 29
# 2017_Jan_Feb_sexorient.tsv 1153 1127
# 29365

# remove lines containing a phrase: grep -v "hatecrime" tmp1 > tmp2