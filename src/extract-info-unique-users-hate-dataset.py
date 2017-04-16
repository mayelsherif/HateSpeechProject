import csv
import os

def extrct_data_unique_users_hate():
    haters_counts = {}
    haters_counts_category = {}
    dirs = {'2016_Jan_Feb_dataset/':29340, '2017_Jan_Feb_dataset/':29365}
    for dir in dirs:
        print dir
        files = os.listdir(maindir + dir)
        outfilename_all = dir.replace('dataset/', 'unq_users.tsv')
        with open(outdir + '/unique-users/' + outfilename_all, "w") as outfile_all:
            w_all = csv.DictWriter(outfile_all, colnames, extrasaction="ignore")
            for file in files:
                if file not in ['2016_Jan_Feb_i_hate.tsv', '2017_Jan_Feb_i_hate.tsv', '2016_Jan_Feb_ht.tsv', '2017_Jan_Feb_ht.tsv']:
                    print file
                    haters_counts_category[file] = {}                 
                    outfilename = file.replace('.tsv', '_unq_users.tsv')
                    with open(maindir + dir + file,'rU') as infile, open(outdir + '/unique-users/' + outfilename, "w") as outfile:
                        r = csv.DictReader((line.replace('\0','') for line in infile), fieldnames =colnames, delimiter="\t")
                        w = csv.DictWriter(outfile, colnames, extrasaction="ignore")
                        for row in r:
                            userid = row['uid']                           
                            if userid not in haters_counts:
                            	w_all.writerow(row)
                                haters_counts[userid] =1
                            else:
                                haters_counts[userid] +=1
                            if userid not in haters_counts_category[file]:
                                w.writerow(row)
                                haters_counts_category[file][userid] = 1
                            else: 
                                haters_counts_category[file][userid] += 1
    print haters_counts_category

    with open(outdir + "haters_count/haters_count_global.txt", "w") as fout:
        for user in haters_counts:
            fout.write(str(user) + "," + str(haters_counts[user]) +"\n")

    for cat in haters_counts_category:
    	cat_name = cat.replace(".tsv", "")
        with open(outdir + "haters_count/haters_count_" + cat_name + ".txt", "w") as fout:
            for user in haters_counts_category[cat]:
                fout.write(str(user) + "," + str(haters_counts_category[cat][user]) +"\n")


extrct_data_unique_users_hate()